#!/usr/bin/env python
import os
import shutil
from setuptools import setup, find_packages

PROJ_NAME = "micropython_hints"
    
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(CUR_PATH, "build")
if os.path.isdir(path):
    print("INFO DEL DIR ", path)
    shutil.rmtree(path)
path = os.path.join(CUR_PATH, "dist")
if os.path.isdir(path):
    print("INFO DEL DIR ", path)
    shutil.rmtree(path)

with open(os.path.join(CUR_PATH, "README.md"), 'r+', encoding='utf8') as f:
    long_description = f.read()

URL = f"https://github.com/miaobuao/{PROJ_NAME}"

setup(
    name         = PROJ_NAME,
    author       =  "miaobuao",
    url          =  URL,
    description  =  "MicroPython type hints",
    version      =  "0.0.6",
    license      =  "MIT License",
    author_email =  "miaobuao@outlook.com",
    long_description     = long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            f'build-hints = {PROJ_NAME}:run',
            f"remove-hints = {PROJ_NAME}:remove"
        ],
    },
    install_requires=[
        'tqdm',
        'meo>=0.1.13'
    ],
)
