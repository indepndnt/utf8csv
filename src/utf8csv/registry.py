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
