import logging
import os
from pathlib import Path
import time
from utf8csv import constants


def prepend(file: Path) -> None:
    """Write source to destination with UTF-8 byte order mark prepended"""
    stub = file.open("rb").read(6)
    if any((stub[:3] == constants.BOM, stub[:4] in constants.OTHER_BOMS_4C, stub[:3] in constants.OTHER_BOMS_3C, stub[:2] in constants.OTHER_BOMS_2C)):
        # Our source file already has a byte order mark!
        return
    original_stat = file.stat()
    original = file.with_name(f"{file.stem}_original{file.suffix}")
    file.rename(original)
    with original.open("rb") as src, file.open("wb") as dst:
        dst.write(constants.BOM)
        while True:
            data = src.read(constants.READ_BLOCK_SIZE)
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
    if file.open("rb").read(3) != constants.BOM:
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
            data = src.read(constants.READ_BLOCK_SIZE)
            if not data:
                break
            dst.write(data)
    original.unlink(missing_ok=True)
    os.utime(file, (original_stat.st_atime, original_stat.st_mtime))
    logging.debug(f"File {file} stripped of BOM")
