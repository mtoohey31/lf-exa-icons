#!/usr/bin/env python3

from setuptools import setup

setup(
    name="lf-exa-icons",
    version="0.1.0",
    url="https://github.com/mtoohey31/lf-exa-icons",
    author="Matthew Toohey",
    author_email="contact@mtoohey.com",
    packages=["lf_exa_icons"],
    entry_points={"console_scripts": ["lf-exa-icons = lf_exa_icons:main"]},
    test_suite='tests',
)
