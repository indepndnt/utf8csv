from setuptools import setup, find_packages

setup(
    name="utf8csv",
    version="2022.05",
    description="Open CSV files in Excel with UTF-8 encoding",
    author="Joe Carey",
    author_email="joecarey001@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pywin32==304"],
)
