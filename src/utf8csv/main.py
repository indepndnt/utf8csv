from argparse import ArgumentParser
import logging
import os
from pathlib import Path
import sys
from utf8csv import constants, excel, modify_file, registry

EXE = sys.executable


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
            # copy this program to %LOCALAPPDATA%\{APPLICATION}
            from shutil import copy, SameFileError

            src = Path(self._program)
            dst = Path(os.getenv("LOCALAPPDATA")) / (constants.APPLICATION + src.suffix)
            try:
                copy(src, dst)
            except SameFileError:
                pass
            self._program = str(dst)
        logging.debug(f"Runner command: {self._command}")
        if dry_run:
            print(f"DefaultIcon: '{registry.get_value(constants.ICON_PATH)}'")
            return
        registry.set_file_type()
        registry.set_prog_id(self._command)
        registry.set_import_default_encoding()
        logging.debug(f"Installed to {self._program}.")

    def uninstall(self, dry_run: bool) -> None:
        """Remove this program as CSV file handler"""
        currently = registry.get_value(".csv")
        if dry_run:
            print(f"Current: '{currently}'")
            return
        if currently != constants.REG_NAME:
            return
        # registry.unset_file_type()  # skip (see function docstring)
        registry.unset_prog_id()
        registry.unset_import_default_encoding()

        # delete this program from %LOCALAPPDATA%\{APPLICATION}
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
            self._xls_assoc = registry.get_open_association(".xlsx")
            logging.debug(f"Identified Excel association command as {self._xls_assoc}.")
        return self._xls_assoc

    def execute(self, file: Path, dry_run: bool = False) -> None:
        """Confirm that arguments are CSV files that exist, then open them"""
        if not file.is_file():
            logging.debug(f"{file} is not a file.")
            return
        if file.suffix.lower() != ".csv":
            logging.debug(f"{file} is not a CSV file.")
            return
        # Rewrite the file starting with the UTF-8 Byte Order Mark
        modify_file.prepend(file)
        if not dry_run:
            # Open the CSV with Excel
            excel.launch(self.excel_association, file)


def main() -> None:
    """Set up CLI arguments and options"""
    log_file = Path(EXE).with_name(f"{constants.APPLICATION}.log")
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
