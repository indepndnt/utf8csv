from pathlib import Path
from setuptools import setup
import sys
sys.path.append(str(Path(__file__).parent))
from info import package_name, version, author, author_email, url, description, requires

setup(
    name=package_name,
    version=version,
    author=author,
    author_email=author_email,
    url=url,
    license=Path(__file__).with_name("LICENSE").read_text(),
    description=description,
    packages=[package_name],
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=requires,
)
