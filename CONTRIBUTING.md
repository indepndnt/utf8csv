# Contributing

Contributions are welcome.

### Getting Started

- Clone repository
```shell
D:\Projects> git clone https://github.com/indepndnt/utf8csv.git
D:\Projects> cd utf8csv
```
The remainder of this document assumes you are in the root project folder.
- Create virtual environment
```shell
D:\Projects\utf8csv> python3 -m venv .venv
D:\Projects\utf8csv> .venv\Scripts\activate
```
- Install dev dependencies
```shell
D:\Projects\utf8csv> python -m pip install pytest black cx_Freeze -e .
```
- Run test suite
```shell
D:\Projects\utf8csv> pytest
```
- run black formatter
```shell
D:\Projects\utf8csv> black -l 120 .
```

### Manual Tests

The automated test suite does not attempt to open Excel or run the GUI, nor does it build the installer, so some 
functionality must be tested manually.

- Check that the GUI opens and looks right, checkboxes respond and scrolling works
```shell
D:\Projects\utf8csv> python src\utf8csv\main.py
```
- Check that Excel opens a CSV file with unicode characters in the correct encoding
```shell
D:\Projects\utf8csv> python src\utf8csv\main.py "C:\Users\you\Downloads\sample.csv"
```
After building and running the installer:
- Check that opening a CSV file with unicode characters from Windows Explorer works correctly
- Check that `utf8csv` is in the Start Menu and opens the GUI correctly

### Building a Distribution

- Ensure version is set in `info.py`. We use [CalVer](https://calver.org/) YYYY.0M.0D (literally
`today().strftime("%Y.%m.%d")`).
- Run cx_Freeze
```shell
D:\Projects\utf8csv> python build.py bdist_msi
```
The output will be a file named like `utf8csv-22.05.22-win64.msi` in a new folder named `dist`.
- Run the installer
```shell
D:\Projects\utf8csv> dist\utf8csv-<yy.mm.dd>-win64.msi
```
