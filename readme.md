# PowerShell Script
Open .csv file with Excel using UTF-8 encoding
```shell
Param([Parameter(Mandatory, HelpMessage = "Specify [path\]filename of CSV file.")][string]$csv_file)
$temp_file = ([string]$csv_file).ToLower().Replace(".csv","_original.csv")
```

# File Type Association - CSV
### Registry:
```
HKEY_CLASSES_ROOT\.csv\
HKEY_LOCAL_MACHINE\SOFTWARE\Classes\.csv\
  (Default)                    REG_SZ  Excel.CSV
  Content Type                 REG_SZ  application/vnd.ms-excel
  Perceived Type               REG_SZ  text
  PersistentHandler\(Default)  REG_SZ  {5e941d80-bf96-11cd-b579-08002b30bfeb}
  OpenWithProgids\(Default)    REG_SZ  (value not set)

HKEY_CURRENT_USER\Software\Classes\.csv\
  (Default)                    REG_SZ  (value not set)
  OpenWithProgids\(Default)    REG_SZ  (value not set)
```

### Set to .ps1 script:
```
cmd /c assoc .csv=csvfile
cmd /c ftype csvfile=powershell.exe -File `"C:\path\to\your.ps1`" `"%1`"
```

# idea:
1) copy file to *_original.csv
2) prepend 0xEF,0xBB,0xBF to beginning of file
3) launch Excel to open modified file
    in separate process (["start", filename]), wait until opening complete
4) delete modified file
5) rename original to original filename

# Bonus: add UTF-8 default for imports
- open RegEdit to HKEY_CURRENT_USER>Software>Microsoft>Office>16.0>Excel>Options
- Right click in the right-hand window and choose New>DWORD
- Call the new DWORD item DefaultCPG and hit enter.
- Then right click on DefaultCPG and choose Modify.
- Set the Base to Decimal, and enter the decimal value for Unicode UTF-8 (65001 in this case), then hit OK.


# Installation Note
After installing, the next time you open a CSV file, Windows may prompt you with
a "How do you want to open .csv files from now on?" window with Excel in the
"Keep using this app" section, and Python listed in the "Other options" section.
Select Python, click the "Always use this program" checkbox and "OK".
