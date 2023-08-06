#!/usr/bin/env python
import sys

from setuptools import find_namespace_packages, setup

if sys.version_info < (3, 7):
    print("Error: Soda Core requires at least Python 3.7")
    print("Error: Please upgrade your Python version to 3.7 or later")
    sys.exit(1)

package_name = "soda-core-pandas-dask"
package_version = "3.0.46"
description = "Soda Core Dask Package"

requires = [f"soda-core=={package_version}", "dask>=2022.10.0", "dask-sql>=2022.12.0,<2023.6.0"]

setup(
    name=package_name,
    version=package_version,
    install_requires=requires,
    packages=find_namespace_packages(include=["soda*"]),
)
