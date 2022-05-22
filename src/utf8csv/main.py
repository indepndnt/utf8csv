import logging
from pathlib import Path
import sys
from utf8csv import excel, language, logs, window


def _file(file: Path, dry_run: bool = False) -> int:
    try:
        return excel.open_csv(file, dry_run)
    except Exception:
        logging.exception(language.text(language.ERR_CSV_CATCH))
        raise


def _gui() -> int:
    try:
        return window.load_gui()
    except Exception:
        logging.exception(language.text(language.ERR_GUI_CATCH))
        raise


def main() -> int:
    """Set up logging and parse CLI arguments"""
    logs.setup()
    logging.debug(f"Call: {sys.argv}")

    # command line
    if len(sys.argv) < 2 or not sys.argv[1]:
        # launch gui
        return _gui()

    # open the file
    return _file(Path(sys.argv[1]))


if __name__ == "__main__":
    sys.exit(main())
