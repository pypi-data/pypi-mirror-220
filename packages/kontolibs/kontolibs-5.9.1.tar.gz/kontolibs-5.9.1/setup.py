import re

import setuptools 

from kynaylibs import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "kontolibs"
author = "bisghav"
version=__version__
author_email = "cosmospanas70@gmail.com"
description = "A Secure and Powerful Python-Pyrogram Based Library For Naya-Pyro."
license_ = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
url = "https://github.com/naya1503/kynaylibs"
project_urls = {
    "Bug Tracker": "https://github.com/naya1503/kynaylibs/issues",
    "Documentation": "https://t.me/kynansupport",
    "Source Code": "https://github.com/naya1503/kynaylibs",
}
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    project_urls=project_urls,
    license=license_,
    packages=setuptools.find_packages(),
    install_requires=["aiosqlite<0.18.0,>=0.16.0", "pyaes==1.6.1", "pysocks==1.7.1", "pytgcalls==3.0.0.dev24", "pytz", "tgcrypto"],
    classifiers=classifiers,
    python_requires=">3.7, <3.12",
)
