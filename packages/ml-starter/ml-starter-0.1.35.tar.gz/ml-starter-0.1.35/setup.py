#!/usr/bin/env python
"""Setup script for the ml-starter project."""

import re

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description: str = f.read()


with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements: list[str] = f.read().splitlines()


with open("requirements-dev.txt", "r", encoding="utf-8") as f:
    requirements_dev: list[str] = f.read().splitlines()


with open("requirements-docs.txt", "r", encoding="utf-8") as f:
    requirements_docs: list[str] = f.read().splitlines()


with open("ml/__init__.py", "r", encoding="utf-8") as fh:
    version_re = re.search(r"^__version__ = \"([^\"]*)\"", fh.read(), re.MULTILINE)
assert version_re is not None, "Could not find version in ml/__init__.py"
version: str = version_re.group(1)


setup(
    name="ml-starter",
    version=version,
    description="ML project template repository",
    author="Benjamin Bolte",
    url="https://github.com/codekansas/ml-starter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    tests_require=requirements_dev,
    extras_require={"dev": requirements_dev, "docs": requirements_docs},
    package_data={"ml": ["py.typed"]},
)
