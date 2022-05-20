import distutils.command.bdist_msi
import msilib
import os
import sysconfig
from cx_Freeze import setup, Executable
from cx_Freeze.windist import bdist_msi as cx_bdist_msi

executable = Executable("src/utf8csv/main.py", base="Win32GUI", icon="media/utf8csv.ico", target_name="utf8csv",)


# In figuring out how to get this to create the installer the way I wanted, I discovered the following
# Microsoft resources:
# - Orca (from Microsoft's [Windows 10 SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/))
#   for modifying MSI files
# - [MSI reference](https://docs.microsoft.com/en-us/windows/win32/msi/installer-database)

class bdist_msi(cx_bdist_msi):
    def add_properties(self):
        metadata = self.distribution.metadata
        # strip the "20" off version number to fit MSI version number constraints:
        #   {major max:255}.{minor max:255}.{build max:65535}
        version = metadata.get_version()[2:]
        props = [
            ("DistVersion", version),
            ("DefaultUIFont", "DlgFont8"),
            ("ErrorDialog", "ErrorDlg"),
            ("Progress1", "Install"),
            ("Progress2", "installs"),
            ("MaintenanceForm_Action", "Repair"),
            ("ALLUSERS", "2"),
            ("MSIINSTALLPERUSER", "1"),
            ("ARPCONTACT", metadata.author_email),
            ("UpgradeCode", "{30290B55-DDFC-4C4D-BDF9-FCE3FC9098CF}"),
            ("ARPPRODUCTICON", "Utf8csvIcon"),
        ]
        msilib.add_data(self.db, "Property", props)
        msilib.add_data(self.db, "Icon", [("Utf8csvIcon", msilib.Binary("media/utf8csv.ico"))])

    def finalize_options(self):
        distutils.command.bdist_msi.bdist_msi.finalize_options(self)
        name = self.distribution.get_name()
        fullname = self.distribution.get_fullname()
        platform = sysconfig.get_platform().replace("win-amd64", "win64")
        program_files_folder = "ProgramFiles64Folder" if "64" in platform else "ProgramFilesFolder"
        # strip the "20" off version number to fit MSI version number constraints:
        #   {major max:255}.{minor max:255}.{build max:65535}
        version = self.distribution.get_version()[2:]
        self.initial_target_dir = fr"[{program_files_folder}]\{name}"
        self.add_to_path = False
        if not fullname.lower().endswith(".msi"):
            fullname = f"{fullname}-{platform}.msi"
        if not os.path.isabs(fullname):
            fullname = os.path.join(self.dist_dir, fullname)
        self.target_name = fullname
        self.directories = []
        self.environment_variables = []
        self.data = {}
        self.summary_data = {}
        self.separate_components = {}
        for idx, executable in enumerate(self.distribution.executables):
            base_name = os.path.basename(executable.target_name)
            self.separate_components[base_name] = msilib.make_id(f"install_{idx}_{executable}")
        executable = "utf8csv.exe"
        component = self.separate_components[executable]
        progid = msilib.make_id(f"{os.path.splitext(executable)[0]}.{version}")
        self._append_to_data("ProgId", progid, None, None, self.distribution.get_description(), "Utf8csvIcon", None)
        self._append_to_data("Extension", "csv", component, progid, "text/csv", "default")
        self._append_to_data("Verb", "csv", "open", 0, "Open with utf8csv and Excel", '"%1"')
        # todo: pr to change "None" to "" in windist.py 873? ICE03 error: invalid guid string
        self._append_to_data("MIME", "text/csv", "csv", "")
        # Registry entries that allow proper display of the app in menu
        # todo: pr to change - to _ in windist.py 877-895? ICE03 error: invalid identifier
        self._append_to_data("Registry", f"{progid}_name", -1, fr"Software\Classes\{progid}", "FriendlyAppName", name, component)
        self._append_to_data("Registry", f"{progid}_verb_open", -1, fr"Software\Classes\{progid}\shell\open", "FriendlyAppName", name, component)
        self._append_to_data("Registry", f"{progid}_author", -1, fr"Software\Classes\{progid}\Application", "ApplicationCompany", self.distribution.get_author(), component)


setup(
    name="utf8csv",
    version="2022.05.20",
    description="Open CSV files in Excel with UTF-8 encoding",
    author="Joe Carey",
    author_email="joecarey001@gmail.com",
    packages=["utf8csv"],
    package_dir={"": "src"},
    install_requires=["pywin32==304"],
    cmdclass={"bdist_msi": bdist_msi},
    options={"build_exe": {"include_msvcr": True}},
    executables=[executable],
)
