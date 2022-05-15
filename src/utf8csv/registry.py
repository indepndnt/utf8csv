import logging
import winreg
from utf8csv import constants


def get_value(key: str) -> str:
    """Find a class-related registry key, searching first current_user, then local_machine, then root"""
    for base, middle in constants.SEARCH_PATHS:
        try:
            if value := winreg.QueryValue(base, f"{middle}\\{key}"):
                return value
        except FileNotFoundError:
            pass
    return ""


def set_file_type() -> None:
    # Record the association in the registry
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{constants.USER_PATH}\\.csv") as k:
        winreg.SetValue(k, "", winreg.REG_SZ, constants.REG_NAME)
        winreg.SetValueEx(k, "Content Type", 0, winreg.REG_SZ, "application/vnd.ms-excel")
        winreg.SetValueEx(k, "PerceivedType", 0, winreg.REG_SZ, "text")
        with winreg.CreateKey(k, "OpenWithProgIds") as open_with:
            winreg.SetValueEx(open_with, constants.REG_NAME, 0, winreg.REG_NONE, b"")


def unset_file_type() -> None:
    keys = [
        f"{constants.USER_PATH}\\.csv\\OpenWithProgIds",
        f"{constants.USER_PATH}\\.csv",
    ]
    for key in keys:
        logging.debug(f"Deleting registry key HKCU\\{key}.")
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key)
        except FileNotFoundError:
            logging.debug(f"Registry key HKCU\\{key} not found, skipping.")


def set_prog_id(open_command: str) -> None:
    # Record command details in the registry
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{constants.USER_PATH}\\{constants.REG_NAME}") as k:
        winreg.SetValue(k, "", winreg.REG_SZ, "Open CSV files with UTF-8 encoding in Excel")
        with winreg.CreateKey(k, "shell\\open\\command") as launch:
            winreg.SetValue(launch, "", winreg.REG_SZ, open_command)
        if icon_path := get_value(constants.ICON_PATH):
            with winreg.CreateKey(k, r"DefaultIcon") as icon:
                winreg.SetValue(icon, "", winreg.REG_SZ, icon_path)


def unset_prog_id() -> None:
    root = f"{constants.USER_PATH}\\{constants.REG_NAME}"
    keys = [
        f"{root}\\shell\\open\\command",
        f"{root}\\shell\\open",
        f"{root}\\shell",
        f"{root}\\DefaultIcon",
        root,
    ]
    for key in keys:
        logging.debug(f"Deleting registry key HKCU\\{key}.")
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key)
        except FileNotFoundError:
            logging.debug(f"Registry key HKCU\\{key} not found, skipping.")


def set_import_default_encoding() -> None:
    if sub_key := excel_options_key():
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, sub_key) as k:
            winreg.SetValueEx(k, "DefaultCPG", 0, winreg.REG_DWORD, 65001)


def unset_import_default_encoding() -> None:
    try:
        if key := excel_options_key():
            logging.debug(f"Deleting HKCU\\{key}\\DefaultCPG")
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_ALL_ACCESS) as k:
                winreg.DeleteValue(k, "DefaultCPG")
    except FileNotFoundError:
        logging.debug(f"Registry value DefaultCPG not found, skipping.")


def get_open_association(suffix: str) -> str:
    """Find the associated open command for a file type"""
    assoc_name = get_value(suffix)
    key = f"{assoc_name}\\shell\\open\\command"
    assoc_command = get_value(key)
    if not assoc_command:
        raise OSError(f"Could not find file association for {suffix}!")
    elif assoc_command[0] == '"':
        end = assoc_command.find('"', 1)
        return assoc_command[1:end]
    else:
        return assoc_command


def excel_options_key() -> str:
    """Iterate over registry key set until one with matching format is found"""
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Office") as k:
        i = 0
        while True:
            try:
                key = winreg.EnumKey(k, i)
            except OSError:
                break
            if key.replace(".", "").isnumeric():
                return f"Software\\Microsoft\\Office\\{key}\\Excel\\Options"
            i += 1
    return ""
