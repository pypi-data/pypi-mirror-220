from setuptools import setup, find_packages

from codecs import open
from os import path

NAME = path.abspath(path.dirname(__file__))

with open(path.join(NAME, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="satsure-ds-utils",
    version="0.1.6",
    description="Common Utilities for SatSure Data Science Team.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://satsure-ds-utils.readthedocs.io/",
    author="SatSure DS Team",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["satsure_ds_utils"],
    include_package_data=True,
    install_requires=[
        "rasterio",
        "geopandas",
        "fiona",
        "scikit-image",
        "pandas",
        "numpy"
    ]
)