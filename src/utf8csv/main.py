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
            # If we exist as a PyInstaller one-file .EXE or cx_Freeze installed .EXE
            self._program = EXE
            self._run_as_script = False
        self._xls_assoc = None

    def __call__(self, file: Path | None, dry_run: bool = False) -> None:
        logging.debug(f"Opening {file}.")
        self.execute(file, dry_run=dry_run)

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
    log_file = Path(os.getenv("LOCALAPPDATA")) / "utf8csv.log"
    logging.basicConfig(filename=log_file, encoding="utf-8", level=logging.DEBUG)
    logging.debug(f"Call: {sys.argv}")
    parser = ArgumentParser(epilog="Thank you for using utf8csv!")
    parser.add_argument("file", help="open this CSV file", type=Path, nargs="?")
    args = parser.parse_args()
    opener = Opener()
    opener(args.file)


if __name__ == "__main__":
    main()
