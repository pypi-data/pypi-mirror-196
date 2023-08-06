from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2.5'
DESCRIPTION = 'package for file storage'
with open("README.md",'r') as fh:
    LONG_DESCRIPTION = fh.read()
# Setting up
setup(
    name="filestostorage",
    version=VERSION,
    author="ngit_kmit",
    author_email="devikarubir@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[ 'rich>=10.12.0',
        'gridfs>=1.10.1',
        'certifi>=2021.5.30',
        'pymongo>=3.12.0'],
    keywords=['mongodb','store files', 'database', 'store', 'file', 'ngit','mongo','kmit'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ]
)
