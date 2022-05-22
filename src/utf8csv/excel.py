import logging
from pathlib import Path
import pythoncom
import subprocess
import time
from utf8csv import language, modify_file, registry, config


def open_csv(file: Path, dry_run: bool = False) -> int:
    """Confirm that arguments are CSV files that exist, then open them"""
    if not file.is_file():
        logging.debug(language.text(language.LOG_NOT_FILE, str(file)))
        return 1
    if file.suffix.lower() != ".csv":
        logging.debug(language.text(language.LOG_NOT_CSV, str(file)))
        return 2
    # Rewrite the file starting with the UTF-8 Byte Order Mark
    modify_file.prepend(file)
    if not dry_run:
        settings = config.get_settings(dry_run=True)
        # Open the CSV with Excel
        launch_excel(file, strip_bom=settings.strip_bom)
    return 0


def launch_excel(file: Path, strip_bom: bool) -> None:
    """Open CSV file with Excel and confirm it has opened"""
    open_command = registry.get_open_association(".xlsx")
    logging.info(language.text(language.LOG_OPEN, open_command, str(file)))
    # launch Excel opening our file, and attempt to strip BOM from file after Excel exits
    subprocess.Popen(f'{open_command} "{file}"')
    await_excel_open(file)
    logging.debug(language.text(language.LOG_IN_EXCEL, str(file)))
    if strip_bom:
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
            raise TimeoutError(language.text(language.ERR_TIMEOUT, filename))
        time.sleep(0.5)
