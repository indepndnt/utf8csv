; // File syntax: https://docs.microsoft.com/en-us/windows/win32/eventlog/sample-message-text-file

MessageIdTypedef=WORD

SeverityNames=(Success=0x0:STATUS_SEVERITY_SUCCESS
Informational=0x1:STATUS_SEVERITY_INFORMATIONAL
Warning=0x2:STATUS_SEVERITY_WARNING
Error=0x3:STATUS_SEVERITY_ERROR
)

LanguageNames=(English=0x409:MSG00409)

; // Message definitions follow.

MessageId=100
Severity=Informational
SymbolicName=INSTALL
Language=English
Installing OpenCSV.
.

MessageId=101
Severity=Informational
SymbolicName=UNINSTALL
Language=English
Uninstalling OpenCSV.
.

MessageId=102
Severity=Informational
SymbolicName=OPEN_FILE
Language=English
Opening %1.
.

MessageId=103
Severity=Informational
SymbolicName=RUNNER_COMMAND
Language=English
Runner command: %1.
.

MessageId=104
Severity=Informational
SymbolicName=OPEN_FILE
Language=English
Opening %1.
.

MessageId=105
Severity=Success
SymbolicName=INSTALL_LOCATION
Language=English
Installed to %1.
.

MessageId=106
Severity=Informational
SymbolicName=DEL_REG_KEY
Language=English
Deleting registry key HKEY_CURRENT_USER\%1.
.

MessageId=107
Severity=Warning
SymbolicName=REG_KEY_NOT_FOUND
Language=English
Registry key HKEY_CURRENT_USER\%1 not found, skipping.
.

MessageId=108
Severity=Informational
SymbolicName=DEL_REG_OPTION_VALUE
Language=English
Deleting HKEY_CURRENT_USER\%1\DefaultCPG.
.

MessageId=109
Severity=Warning
SymbolicName=REG_VALUE_NOT_FOUND
Language=English
Registry value DefaultCPG not found, skipping.
.

MessageId=110
Severity=Success
SymbolicName=UNINSTALLED
Language=English
Uninstalled.
.

MessageId=111
Severity=Informational
SymbolicName=EXCEL_COMMAND
Language=English
Identified Excel association command as %1.
.

MessageId=112
Severity=Error
SymbolicName=NOT_A_FILE
Language=English
%1 is not a file.
.

MessageId=113
Severity=Error
SymbolicName=NOT_CSV_FILE
Language=English
%1 is not a CSV file.
.

MessageId=114
Severity=Informational
SymbolicName=OPEN_COMMAND_FILE
Language=English
Opening: %1 "%2".
.

MessageId=115
Severity=Success
SymbolicName=IS_OPEN
Language=English
%1 is open in Excel!
.

MessageId=116
Severity=Success
SymbolicName=ADDED_BOM
Language=English
Added BOM to %1.
.

MessageId=117
Severity=Informational
SymbolicName=WATCHING
Language=English
Started watching to strip %1.
.

MessageId=118
Severity=Warning
SymbolicName=GONE
Language=English
%1 is gone!
.

MessageId=119
Severity=Error
SymbolicName=TIMEOUT
Language=English
Timeout waiting for %1 to close!
.

MessageId=120
Severity=Informational
SymbolicName=NO_BOM
Language=English
No BOM found on %1.
.

MessageId=121
Severity=Success
SymbolicName=STRIPPED_BOM
Language=English
File %1 stripped of BOM.
.
