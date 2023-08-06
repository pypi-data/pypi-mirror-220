#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()
setup(
    name="sahayakAI",
    version="0.0.1",
    description="Sahayak toolkit for India specif use cases",  # short description
    long_description=readme,  # long description from the readme file
    license="PandoraaBox Internal",
    author="PandoraaBox",
    author_email="sahayak@pandoraabox.com",
    url="https://github.com/PandoraaBox/sahayakAI",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pydantic",
        "requests",
        "simpleaichat",
        "python-telegram-bot",
        "pyyaml",
        "fastapi",
        "uvicorn[standard]"
    ]
)
