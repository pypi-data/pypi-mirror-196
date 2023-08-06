#This file contains metadata about the distribution

from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="custom_nester",
    version="1.2.0",
    py_modules      =['custom_nester'],
    description="A simple printer of nested lists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arielden/",
    author="arielden",
    author_email="arieldenaro@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)