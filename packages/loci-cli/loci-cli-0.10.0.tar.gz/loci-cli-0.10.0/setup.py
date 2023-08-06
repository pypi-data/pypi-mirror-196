import os
import setuptools
from loci_cli import PROG_DESC

# This code prevents a circular import. From https://github.com/psf/requests/blob/main/setup.py
about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "loci", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loci-cli",
    author="TheTwitchy",
    version=about["__version__"],
    author_email="thetwitchy@thetwitchy.com",
    description=PROG_DESC,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/loci-notes/loci-cli",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "requests",
        "rich",
        "pendulum"
    ],
    entry_points={
        "console_scripts": [
            "loci = loci_cli.main:root_entry",
        ],
    },
)
