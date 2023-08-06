from setuptools import setup, find_packages
import io
import os
import re

VERSION = "0.0.6"
DESCRIPTION = "XTB broker models, methods and tools"
LONG_DESCRIPTION = DESCRIPTION

setup(
    name="xtb_broker",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Arrubo",
    url="https://pypi.org/project/xtb-broker/",
    packages=find_packages()
)
