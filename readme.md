# Installation Note
After installing, the next time you open a CSV file, Windows may prompt you with
a "How do you want to open .csv files from now on?" window with Excel in the
"Keep using this app" section, and Python listed in the "Other options" section.
Select Python, click the "Always use this program" checkbox and "OK".

# Development

### Setup
- Clone repository
- Create virtual environment
- `python -m pip install pytest black pyinstaller -e .`

### Format
```shell
black -l 120 project\utf8csv
```

### Test
```shell
pytest
```

# Build

### Creating .exe file with PyInstaller
```shell
# CD to project directory
cd project\utf8csv
# run PyInstaller
pyinstaller.exe --onefile --noconfirm --ascii --windowed --name utf8csv .\src\utf8csv\main.py
# ... or ...
pyinstaller.exe --onefile utf8csv.spec
```

# Roadmap
- update logging (maybe file rotate)
- add simple tkinter windows for install/uninstall/options/(view logs)
- options: import encoding default on/off
- options: strip bom after close on/off
