from pathlib import Path
import setuptools

long_desc = Path("README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="holamundopip",
    version="0.0.1",
    long_description=long_desc,
    packages=setuptools.find_packages(exclude=["mocks", "tests"])

)
