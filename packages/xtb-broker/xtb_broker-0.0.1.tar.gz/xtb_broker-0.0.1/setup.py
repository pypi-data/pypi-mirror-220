from setuptools import setup, find_packages
import io
import os
import re
from typing import List

VERSION: str = "0.0.1"


def read(file_name: str):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name), encoding='utf-8') as f:
        return f.read()


setup(
    name="xtb_broker",
    version=VERSION,
    description="XTB broker models, methods and tools",
    author="Arrubo",
    url="https://globaldevtools.bbva.com/bitbucket/projects/SEMAAS/repos/billing-mediation-utils",
    packages=find_packages(),
    install_requires=[],
)
