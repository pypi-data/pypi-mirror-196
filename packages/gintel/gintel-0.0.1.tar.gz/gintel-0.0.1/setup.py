import atexit
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
from urllib.request import urlretrieve


def post_install():
    package_files = Path.home() / ".gintel"
    if not Path(package_files).exists():
        Path(package_files).mkdir()
        urlretrieve(
            "https://raw.githubusercontent.com/harttraveller/gintel/main/files/tokens.json",
            package_files / "tokens.json",
        )


class Installation(install):
    def __init__(self, *args, **kwargs):
        super(Installation, self).__init__(*args, **kwargs)
        atexit.register(post_install)


setup(
    name="gintel",
    version="0.0.1",
    author="Hart Traveller",
    url="https://github.com/harttraveller/gintel",
    license="MIT",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click", "requests", "pyeio", "pillow", "rich"],
    entry_points={"console_scripts": ["gintel=gintel.cli:entry"]},
    cmdclass={
        "install": Installation,
    },
)
