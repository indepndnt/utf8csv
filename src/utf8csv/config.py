import json
import os
from pathlib import Path
import sys

SETTINGS = None


class Settings:
    __valid_settings = {"strip_bom"}

    def __init__(self, dry_run: bool):
        # defaults
        self.strip_bom = True
        # read config file and overwrite defaults if file and settings exist
        self.__dry_run = dry_run
        self.__config_file = Path(os.getenv("LOCALAPPDATA")) / "utf8csv.json"
        if getattr(sys, "frozen", False):
            self.icon_bitmap = Path(sys.executable).parent / "utf8csv.ico"
        else:
            self.icon_bitmap = Path(__file__).parent.parent / "media" / "utf8csv.ico"

        if not self.__config_file.is_file():
            self.save()
            return
        values = json.loads(self.__config_file.read_bytes())
        for key, value in values.items():
            if key not in Settings.__valid_settings:
                continue
            setattr(self, key, value)

    def save(self) -> None:
        if self.__dry_run:
            return
        values = {key: getattr(self, key, None) for key in Settings.__valid_settings}
        self.__config_file.write_text(json.dumps(values))


def get_settings(dry_run: bool = False):
    global SETTINGS
    if SETTINGS is None:
        SETTINGS = Settings(dry_run)
    return SETTINGS
