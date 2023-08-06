from setuptools import setup, find_packages

setup(
    name="filestostorage",
    version="0.0.2.7",
    author="ngit_kmit",
    author_email="devikarubir@gmail.com",
    description="package for file storage",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "gridfs",
        "certifi",
        "pymongo"
    ],
    keywords=[
        "mongodb",
        "store files",
        "database",
        "store",
        "file",
        "ngit",
        "mongo",
        "kmit"
    ],
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
    ],
)
