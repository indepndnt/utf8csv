from winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_CLASSES_ROOT

READ_BLOCK_SIZE = 1024
# The UTF-8 Byte Order Mark
BOM = b"\xef\xbb\xbf"
# Other Byte Order Marks (https://en.wikipedia.org/wiki/Byte_order_mark)
OTHER_BOMS_2C = {
    b"\xfe\xff",  # UTF-16 (big endian)
    b"\xff\xfe",  # UTF-16 (little endian)
}
OTHER_BOMS_3C = {
    b"\x2b\x2f\x76",  # UTF-7
    b"\xf7\x64\x4c",  # UTF-1
    b"\x0e\xfe\xff",  # SCSU
    b"\xfb\xee\x28",  # BOCU-1
}
OTHER_BOMS_4C = {
    b"\x00\x00\xfe\xff",  # UTF-32 (big endian)
    b"\xff\xfe\x00\x00",  # UTF-32 (little endian)
    b"\xdd\x73\x66\x73",  # UTF-EBCDIC
    b"\x84\x31\x95\x33",  # GB-18030
}

APPLICATION = "utf8csv"
COMPONENT = "opener"
VERSION = "1"
REG_NAME = ".".join((APPLICATION, COMPONENT, VERSION))

ICON_PATH = "Excel.CSV\\DefaultIcon"
USER_PATH = "Software\\Classes"
SEARCH_PATHS = [(HKEY_CURRENT_USER, USER_PATH), (HKEY_LOCAL_MACHINE, "SOFTWARE\\Classes"), (HKEY_CLASSES_ROOT, "")]
