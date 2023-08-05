from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Finance functions'
LONG_DESCRIPTION = 'A package that allows to do get and manipulate finance related data from web, focused on brazilian stock market.'

# Setting up
setup(
    name="financelibje",
    version=VERSION,
    author="joaoope11 (João Pedro Eduardo)",
    author_email="<joaopqeduardo@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
