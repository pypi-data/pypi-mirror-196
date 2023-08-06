from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="gintel",
    version="0.0.0",
    author="Hart Traveller",
    url="https://github.com/harttraveller/gintel",
    license="MIT",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click", "requests"],
    entry_points={"console_scripts": ["gintel=gintel.cli:entry"]},
)
