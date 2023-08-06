#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import setuptools

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('rrmscorer/__main__.py').read(),
    re.M
    ).group(1)


# parent_path = os.path.relpath(".")
# path_to_file = os.path.join(parent_path, "README.md")

with open("README_pip.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="rrmscorer",
    version=version,
    corresponding_author="Wim Vranken",
    corresponding_author_email="Wim.Vranken@vub.be",
    description="RRM-RNA score predictor",
    license="OSI Approved :: GNU General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Joel Roca-Martinez, Wim Vranken",
    maintainer_email="joel.roca.martinez@vub.be, wim.vranken@vub.be",
    url="",
    packages=setuptools.find_packages(include=['rrmscorer']),
    include_package_data=True,
    keywords="proteins,RRM,RNA,predictor,sequence",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable"
    ],

    python_requires=">=3.9",

    install_requires=[
        "biopython",
        "numpy",
        "pandas",
        "requests",
        "scikit-learn",
        "matplotlib",
        "logomaker"
    ]
)
