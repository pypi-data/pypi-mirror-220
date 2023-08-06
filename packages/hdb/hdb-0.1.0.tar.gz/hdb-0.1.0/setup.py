import hdb
from setuptools import setup, find_packages

setup(
    name="hdb",
    version="0.1.0",
    author="Chris Varga",
    author_email="",
    description="Persistent, hobbit-sized dictionaries",
    long_description=hdb.__doc__,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="hdb dictionary json persistent hobbit database",
)
