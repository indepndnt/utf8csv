import logging
from pathlib import Path
import pythoncom
import subprocess
import time
from utf8csv import modify_file


def launch(open_command: str, file: Path) -> None:
    """Open CSV file with Excel and confirm it has opened"""
    logging.debug(f'Opening: {open_command} "{file}"')
    # launch Excel opening our file, and attempt to strip BOM from file after Excel exits
    subprocess.Popen(f'{open_command} "{file}"')
    await_excel_open(file)
    logging.debug(f"{file} is open in Excel!")
    # once open, wait for it to close and strip the BOM
    modify_file.strip_bom(file)


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
