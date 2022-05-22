version = "2022.05.22"

package_name = "utf8csv"
# strip the "20" off version number to fit MSI version number constraints:
#   {major max:255}.{minor max:255}.{build max:65535}
msi_version = version[2:]
author = "Joe Carey"
author_email = "joecarey001@gmail.com"
url = "https://github.com/indepndnt/utf8csv"
description = "Open CSV files in Excel with UTF-8 encoding"
download_url = "https://github.com/indepndnt/utf8csv/releases/"
requires = ["pywin32==304"]
