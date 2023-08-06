# -*- coding: utf-8 -*-
import os
from distutils.core import setup

from setuptools import find_packages, setup


def read(fname):
    with open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), fname),
        "r",
        encoding="utf-8",
    ) as fin:
        return fin.read()


setup(
    name="dspawpy",
    version="1.0.4",
    packages=find_packages(),
    url="http://www.hzwtech.com/",
    license="MIT",
    author="Hzwtech",
    author_email="ZhengZhilin@hzwtech.com",
    description="Tools for dspaw",
    install_requires=[
        "pymatgen>=2021.2.8.1",
        "statsmodels>=0.12.0",
        "h5py >= 3.7",
    ],
    python_requires=">=3.6",
    entry_points={},
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
)
