import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "foxy",
    version = "0.0.1",
    author = "David Holiday",
    author_email = "david.holiday@clickfox.com",
    description = ("a rad dashboard for local docker development."),
    license = "MIT",
    keywords = "docker dashboard gui rad",
    url = "http://www.clickfox.com",
    packages=find_packages(),
    install_requires=['cherrypy'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)