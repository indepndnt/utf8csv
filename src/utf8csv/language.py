import locale

LANGUAGE = locale.getdefaultlocale()[0]

OPTION_LABEL = {
    "en_US": "Utf8csv Options",
}
LOGS_LABEL = {
    "en_US": "Recent Logs",
}
CLOSE = {
    "en_US": "Close",
}
EXCEL_OPT = {
    "en_US": "Set Excel import CSV default encoding option to UTF-8",
}
STRIP_OPT = {
    "en_US": "Remove the added BOM characters after Excel releases the CSV file",
}
LOG_OPEN = {
    "en_US": 'Opening: %1 "%2"',
}
LOG_NOT_FILE = {
    "en_US": "%1 is not a file.",
}
LOG_NOT_CSV = {
    "en_US": "%1 is not a CSV file.",
}
LOG_IN_EXCEL = {
    "en_US": "%1 is open in Excel!",
}
ERR_TIMEOUT = {
    "en_US": "Timeout waiting for Excel to open %1",
}
LOG_ADDED = {
    "en_US": "Added BOM to %1",
}
LOG_WATCHING = {
    "en_US": "Started watching to strip %1",
}
LOG_GONE = {
    "en_US": "File %1 is gone!",
}
LOG_TIMEOUT = {
    "en_US": "Timout waiting for %1 to close!",
}
LOG_NO_BOM = {
    "en_US": "No UTF-8 BOM found on %1",
}
LOG_STRIPPED = {
    "en_US": "File %1 stripped of BOM",
}
LOG_DELETING = {
    "en_US": r"Deleting HKCU\%1\DefaultCPG",
}
LOG_CPG_NOT_FOUND = {
    "en_US": "Registry value DefaultCPG not found, skipping.",
}
ERR_NO_ASSOC = {
    "en_US": "Could not find file association for %1!",
}
ERR_CSV_CATCH = {
    "en_US": "Exception raised when opening file!",
}
ERR_GUI_CATCH = {
    "en_US": "Exception raise from GUI!",
}


def text(selector: dict[str, str], *replacements: str) -> str:
    value = selector.get(LANGUAGE, "en_US")
    for i, arg in enumerate(replacements, 1):
        value = value.replace(f"%{i}", arg)
    return value
