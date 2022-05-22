import distutils.command.bdist_msi
import msilib
import os
from pathlib import Path
import sys
import sysconfig
from cx_Freeze import setup, Executable
from cx_Freeze.windist import bdist_msi as cx_bdist_msi

sys.path.append(str(Path(__file__).parent))
from info import version, msi_version, package_name, author, author_email, url, description, download_url, requires

executable = Executable(
    "src/utf8csv/main.py",
    base="Win32GUI",
    icon="media/utf8csv.ico",
    target_name=package_name,
    shortcut_name="Utf8csv",
    shortcut_dir="StartMenuFolder",
)
build_exe_options = {
    "include_msvcr": True,
    "excludes": ["asyncio", "email", "html", "http", "pydoc_data", "unittest"],
    "include_files": ["media/utf8csv.ico"],
}

# In figuring out how to get this to create the installer the way I wanted, I discovered the following
# Microsoft resources:
# - Orca (from Microsoft's [Windows 10 SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/))
#   for modifying MSI files
# - [MSI reference](https://docs.microsoft.com/en-us/windows/win32/msi/installer-database)


class bdist_msi(cx_bdist_msi):
    def add_properties(self):
        props = [
            ("DistVersion", msi_version),
            ("DefaultUIFont", "DlgFont8"),
            ("ErrorDialog", "ErrorDlg"),
            ("Progress1", "Install"),
            ("Progress2", "installs"),
            ("MaintenanceForm_Action", "Repair"),
            ("ALLUSERS", "2"),
            ("MSIINSTALLPERUSER", "1"),
            ("ARPCONTACT", author_email),
            ("ARPURLINFOABOUT", url),
            ("UpgradeCode", "{30290B55-DDFC-4C4D-BDF9-FCE3FC9098CF}"),
            ("ARPPRODUCTICON", "Utf8csvIcon"),
        ]
        msilib.add_data(self.db, "Property", props)
        msilib.add_data(self.db, "Icon", [("Utf8csvIcon", msilib.Binary("media/utf8csv.ico"))])

    def finalize_options(self):
        distutils.command.bdist_msi.bdist_msi.finalize_options(self)
        platform = sysconfig.get_platform().replace("win-amd64", "win64")
        program_files_folder = "ProgramFiles64Folder" if "64" in platform else "ProgramFilesFolder"
        self.initial_target_dir = rf"[{program_files_folder}]\{package_name}"
        self.add_to_path = False
        self.target_name = os.path.join(self.dist_dir, f"{package_name}-{msi_version}-{platform}.msi")
        self.directories = []
        self.environment_variables = []
        self.data = {}
        self.summary_data = {}
        self.separate_components = {}
        for idx, executable in enumerate(self.distribution.executables):
            base_name = os.path.basename(executable.target_name)
            self.separate_components[base_name] = msilib.make_id(f"install_{idx}_{executable}")
        executable = f"{package_name}.exe"
        component = self.separate_components[executable]
        progid = msilib.make_id(f"{os.path.splitext(executable)[0]}.{msi_version}")
        self._append_to_data("ProgId", progid, None, None, self.distribution.get_description(), "Utf8csvIcon", None)
        self._append_to_data("Extension", "csv", component, progid, "text/csv", "default")
        self._append_to_data("Verb", "csv", "open", 0, "Open with utf8csv and Excel", '"%1"')
        # change "None" to "" in windist.py 873: Orca validation message "ICE03 error: invalid guid string"
        self._append_to_data("MIME", "text/csv", "csv", "")
        # Registry entries that allow proper display of the app in menu
        # change "-" to "_" in windist.py 877-895: Orca validation message "ICE03 error: invalid identifier"
        self._append_to_data(
            "Registry",
            f"{progid}_name",
            -1,
            rf"Software\Classes\{progid}",
            "FriendlyAppName",
            package_name,
            component,
        )
        self._append_to_data(
            "Registry",
            f"{progid}_verb_open",
            -1,
            rf"Software\Classes\{progid}\shell\open",
            "FriendlyAppName",
            package_name,
            component,
        )
        self._append_to_data(
            "Registry",
            f"{progid}_author",
            -1,
            rf"Software\Classes\{progid}\Application",
            "ApplicationCompany",
            "Open Source",
            component,
        )


setup(
    name=package_name,
    version=version,
    author=author,
    author_email=author_email,
    url=url,
    license=Path(__file__).with_name("LICENSE").read_text(),
    description=description,
    download_url=download_url,
    packages=[package_name],
    package_dir={"": "src"},
    install_requires=requires,
    python_requires=">=3.9",
    cmdclass={"bdist_msi": bdist_msi},
    options={"build_exe": build_exe_options},
    executables=[executable],
)
