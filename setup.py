#! python
from setuptools import setup, find_packages

setup(
    name = "flashcookies",
    version = "0.0.1",
    description = "flashcookies shell tool",
    long_description = """
        A shell tool to manipualte Flash cookies (.sol Flash SharedObject files).
    """,
    url = "http://github.com/dsc/flashcookies",
    
    author = "David Schoonover",
    author_email = "dsc@less.ly",
    
    packages=['flashcookies'],
    zip_safe = True,
    install_requires=[
        "pyamf>=0.5.1",
        "pyyaml>=3.08",
    ],
    entry_points={
        'console_scripts': ['flashcookies = flashcookies:main']
    },
    classifiers = [],
)
