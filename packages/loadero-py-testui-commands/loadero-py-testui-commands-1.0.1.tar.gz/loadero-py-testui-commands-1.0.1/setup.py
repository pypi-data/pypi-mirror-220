"""Loadero-Py-TestUI-Commands setup module"""

import pathlib
from setuptools import find_packages, setup


root_path = pathlib.Path(__file__).parent.resolve()
long_description = (root_path / "README.md").read_text(encoding="utf-8")


setup(
    name="loadero-py-testui-commands",
    version="1.0.1",
    description="PyTestUI commands for Loadero scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loadero/loadero-py-testui-commands",
    author="Loadero Team",
    author_email="support@loadero.com",
    license="GPLv3",
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="loadero",
    project_urls={
        "Source": "https://github.com/loadero/loadero-py-testui-commands",
        "Tracker": "https://github.com/loadero/loadero-py-testui-commands/issues",
        "Loadero": "https://loadero.com/",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.6, <4",
    install_requires=[
        "python_testui",
    ],
)
