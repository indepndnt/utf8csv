from setuptools import setup, find_packages

setup(
    name="openCSV",
    version="2022.05",
    description="Open CSV file with UTF-8 encoding",
    author="Joe Carey",
    author_email="joe@python.org",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pywin32==304"],
    entry_points={"console_scripts": ["opencsv = opencsv.main:main"]},
)
