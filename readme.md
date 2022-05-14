# Installation Note
After installing, the next time you open a CSV file, Windows may prompt you with
a "How do you want to open .csv files from now on?" window with Excel in the
"Keep using this app" section, and Python listed in the "Other options" section.
Select Python, click the "Always use this program" checkbox and "OK".

# Development

### Setup
- Clone repository
- Create virtual environment
- `python -m pip install pytest black -e .`

### Format
```shell
black -l 120 D:\PycharmProjects\openCSV
```

### Test
```shell
pytest
```

# Build

### Compiling `eventlog.mc` into `eventlog.dll`

First install Microsoft Visual Studio Community with the C++ and Windows SDK options.
On my system, `mc.exe` and `rc.exe` are then found at
`C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x86\`, and `link.exe` is found at
`C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.32.31326\bin\HostX86\x86\`.

In Visual Studio Community, go to `Tools > Command Line > Developer Command Prompt` to
run these commands, they will be on the path.

```shell
# CD to project directory
cd /project/openCSV
# Compile messages file to .rc/.bin files
mc.exe src/eventlog.mc
# Compile those files to resource file
rc.exe /r eventlog.rc
# Link resource file to dll file
link.exe -dll -noentry -out:src/eventlog.dll eventlog.res
# remove intermediate files
rm eventlog.* MSG*.bin
```

### Creating .exe file
```shell
# CD to project directory
cd project\openCSV
# run PyInstaller
pyinstaller.exe --onefile --noconfirm --ascii --windowed --name opencsv --add-binary "src\eventlog.dll;eventlog.dll" .\src\opencsv\main.py
# ... or ...
pyinstaller.exe --onefile opencsv.spec
```
