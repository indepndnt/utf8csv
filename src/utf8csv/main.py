from argparse import ArgumentParser
import logging
import os
from pathlib import Path
import pythoncom
import subprocess
import sys
import time
from winreg import (
    HKEY_CURRENT_USER,
    HKEY_LOCAL_MACHINE,
    HKEY_CLASSES_ROOT,
    REG_SZ,
    REG_NONE,
    REG_DWORD,
    CreateKey,
    OpenKey,
    EnumKey,
    SetValue,
    SetValueEx,
    QueryValue,
    DeleteKey,
    DeleteValue,
    KEY_ALL_ACCESS,
)

EXE = sys.executable
REG_NAME = "utf8csv"
ICON_PATH = "Excel.CSV\\DefaultIcon"
USER_PATH = "Software\\Classes"
SEARCH_PATHS = [(HKEY_CURRENT_USER, USER_PATH), (HKEY_LOCAL_MACHINE, "SOFTWARE\\Classes"), (HKEY_CLASSES_ROOT, "")]
READ_BLOCK_SIZE = 1024
BOM = b"\xef\xbb\xbf"


class Opener:
    def __init__(self):
        if EXE.endswith("python.exe"):
            # If we exist as a python script run by a Python executable
            self._program = f'{EXE[:-10]}pythonw.exe "{__file__}"'
            self._run_as_script = True
        else:
            # If we exist as a PyInstaller one-file .EXE
            self._program = EXE
            self._run_as_script = False
        self._xls_assoc = None

    def __call__(self, file: Path | None, uninstall: bool, dry_run: bool = False) -> None:
        if uninstall:
            logging.debug("Uninstalling!")
            self.uninstall(dry_run=dry_run)
            return
        if not file:
            logging.debug("Installing!")
            self.setup(dry_run=dry_run)
            return
        logging.debug(f"Opening {file}.")
        self.execute(file, dry_run=dry_run)

    def setup(self, dry_run: bool) -> None:
        """Set this program as the default handler for CSV files"""
        if not self._run_as_script:
            # copy this program to %LOCALAPPDATA%\{REG_NAME}
            from shutil import copy, SameFileError

            src = Path(self._program)
            dst = Path(os.getenv("LOCALAPPDATA")) / (REG_NAME + src.suffix)
            try:
                copy(src, dst)
            except SameFileError:
                pass
            self._program = str(dst)
        logging.debug(f"Runner command: {self._command}")
        if dry_run:
            print(f"DefaultIcon: '{get_registry_value(ICON_PATH)}'")
            return
        # Record the association in the registry
        with CreateKey(HKEY_CURRENT_USER, f"{USER_PATH}\\.csv") as k:
            SetValue(k, "", REG_SZ, REG_NAME)
            SetValueEx(k, "Content Type", 0, REG_SZ, "application/vnd.ms-excel")
            SetValueEx(k, "PerceivedType", 0, REG_SZ, "text")
            with CreateKey(k, "OpenWithProgIds") as open_with:
                SetValueEx(open_with, REG_NAME, 0, REG_NONE, b"")

        # Record command details in the registry
        with CreateKey(HKEY_CURRENT_USER, f"{USER_PATH}\\{REG_NAME}") as k:
            SetValue(k, "", REG_SZ, "Open CSV files with UTF-8 encoding in Excel")
            with CreateKey(k, "shell\\open\\command") as launch:
                SetValue(launch, "", REG_SZ, self._command)
            if icon_path := get_registry_value(ICON_PATH):
                with CreateKey(k, r"DefaultIcon") as icon:
                    SetValue(icon, "", REG_SZ, icon_path)

        # Set Excel default text import encoding to UTF-8
        if sub_key := self.excel_options_key:
            with CreateKey(HKEY_CURRENT_USER, sub_key) as k:
                SetValueEx(k, "DefaultCPG", 0, REG_DWORD, 65001)
        logging.debug(f"Installed to {self._program}.")

    def uninstall(self, dry_run: bool) -> None:
        """Remove this program as CSV file handler"""
        currently = get_registry_value(".csv")
        if dry_run:
            print(f"Current: '{currently}'")
            return
        if currently != REG_NAME:
            return
        root = f"{USER_PATH}\\{REG_NAME}"
        keys = [
            f"{USER_PATH}\\.csv\\OpenWithProgIds",
            f"{USER_PATH}\\.csv",
            f"{root}\\shell\\open\\command",
            f"{root}\\shell\\open",
            f"{root}\\shell",
            f"{root}\\DefaultIcon",
            root,
        ]
        for key in keys:
            logging.debug(f"Deleting registry key HKEY_CURRENT_USER\\{key}.")
            try:
                DeleteKey(HKEY_CURRENT_USER, key)
            except FileNotFoundError:
                logging.debug(f"Registry key HKEY_CURRENT_USER\\{key} not found, skipping.")
        try:
            if key := self.excel_options_key:
                logging.debug(f"Deleting HKEY_CURRENT_USER\\{key}\\DefaultCPG")
                with OpenKey(HKEY_CURRENT_USER, key, 0, KEY_ALL_ACCESS) as k:
                    DeleteValue(k, "DefaultCPG")
        except FileNotFoundError:
            logging.debug(f"Registry value DefaultCPG not found, skipping.")

        # delete this program from %LOCALAPPDATA%\{REG_NAME}
        local_path = os.getenv("LOCALAPPDATA")
        if not self._run_as_script and self._program.startswith(local_path):
            Path(self._program).unlink(missing_ok=True)
        logging.debug("Uninstalled.")

    @property
    def _command(self):
        return f'{self._program} "%1"'

    @property
    def excel_association(self) -> str:
        """Find the command associated with Excel files since we've overridden the CSV association"""
        if self._xls_assoc is None:
            assoc_name = get_registry_value(".xlsx")
            key = f"{assoc_name}\\shell\\open\\command"
            assoc_command = get_registry_value(key)
            if not assoc_command:
                raise OSError("Could not find Excel instance!")
            elif assoc_command[0] == '"':
                end = assoc_command.find('"', 1)
                self._xls_assoc = assoc_command[1:end]
            else:
                self._xls_assoc = assoc_command
            logging.debug(f"Identified Excel association command as {self._xls_assoc}.")
        return self._xls_assoc

    @property
    def excel_options_key(self) -> str:
        """Iterate over registry key set until one with matching format is found"""
        with OpenKey(HKEY_CURRENT_USER, "Software\\Microsoft\\Office") as k:
            i = 0
            while True:
                try:
                    key = EnumKey(k, i)
                except OSError:
                    break
                if key.replace(".", "").isnumeric():
                    return f"Software\\Microsoft\\Office\\{key}\\Excel\\Options"
                i += 1
        return ""

    def execute(self, file: Path, dry_run: bool = False) -> None:
        """Confirm that arguments are CSV files that exist, then open them"""
        if not file.is_file():
            logging.debug(f"{file} is not a file.")
            return
        if file.suffix.lower() != ".csv":
            logging.debug(f"{file} is not a CSV file.")
            return
        # Rewrite the file starting with the UTF-8 Byte Order Mark
        prepend(file)
        if not dry_run:
            # Open the CSV with Excel
            self.launch(file)

    def launch(self, file: Path) -> None:
        """Open CSV file with Excel and confirm it has opened"""
        command = self.excel_association
        logging.debug(f'Opening: {command} "{file}"')
        # launch Excel opening our file, and attempt to strip BOM from file after Excel exits
        subprocess.Popen(f'{command} "{file}"')
        await_excel_open(file)
        logging.debug(f"{file} is open in Excel!")
        # once open, wait for it to close and strip the BOM
        strip_bom(file)


def await_excel_open(file: Path) -> None:
    """Using pywin32, search Running Object Table for Excel with current file open"""
    filename = file.name
    timeout = time.time() + 30
    while True:
        context = pythoncom.CreateBindCtx(0)
        for moniker in pythoncom.GetRunningObjectTable():
            name = moniker.GetDisplayName(context, None)
            if name.endswith(filename):
                time.sleep(0.5)
                return
        if time.time() > timeout:
            raise TimeoutError(f"Timeout waiting for Excel to open {filename}.")
        time.sleep(0.5)


def get_registry_value(key: str) -> str:
    """Find a class-related registry key, searching first current_user, then local_machine, then root"""
    for base, middle in SEARCH_PATHS:
        try:
            if value := QueryValue(base, f"{middle}\\{key}"):
                return value
        except FileNotFoundError:
            pass
    return ""


def prepend(file: Path) -> None:
    """Write source to destination with UTF-8 byte order mark prepended"""
    if file.open("rb").read(3) == BOM:
        # Our source file already has a byte order mark!
        return
    original_stat = file.stat()
    original = file.with_name(f"{file.stem}_original{file.suffix}")
    file.rename(original)
    with original.open("rb") as src, file.open("wb") as dst:
        dst.write(BOM)
        while True:
            data = src.read(READ_BLOCK_SIZE)
            if not data:
                break
            dst.write(data)
    original.unlink(missing_ok=True)
    os.utime(file, (original_stat.st_atime, original_stat.st_mtime))
    logging.debug(f"Added BOM to {file}.")


def strip_bom(file: Path):
    """Rewrite file with UTF-8 byte order mark removed after it's closed"""
    # wait for the file to be closed (up to a max 24hr)
    logging.debug(f"Started watching to strip {file}")
    timeout = time.time() + 86400
    while True:
        if not file.is_file():
            # file is gone? ok
            logging.debug(f"File {file} is gone!")
            return
        try:
            file.rename(file)
            break
        except PermissionError:
            pass
        if time.time() > timeout:
            logging.debug(f"Timout waiting for {file} to close!")
            return
        time.sleep(2)
    # see if the file has a BOM to strip off
    if file.open("rb").read(3) != BOM:
        logging.debug(f"No BOM found on {file}")
        return
    # rewrite the file without the BOM
    original_stat = file.stat()
    original = file.with_name(f"{file.stem}_original{file.suffix}")
    file.rename(original)
    with original.open("rb") as src, file.open("wb") as dst:
        # skip the 3-byte BOM
        src.seek(3)
        while True:
            data = src.read(READ_BLOCK_SIZE)
            if not data:
                break
            dst.write(data)
    original.unlink(missing_ok=True)
    os.utime(file, (original_stat.st_atime, original_stat.st_mtime))
    logging.debug(f"File {file} stripped of BOM")


def main() -> None:
    """Set up CLI arguments and options"""
    log_file = Path(EXE).with_name("utf8csv.log")
    logging.basicConfig(filename=log_file, encoding="utf-8", level=logging.WARNING)
    logging.debug(f"Call: {sys.argv}")
    parser = ArgumentParser(epilog="Thank you for using utf8csv!")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("file", help="open this CSV file", type=Path, nargs="?")
    group.add_argument("-u", "--uninstall", help="remove CSV file association", action="store_true")
    args = parser.parse_args()
    opener = Opener()
    opener(args.file, args.uninstall)


if __name__ == "__main__":
    main()
