#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="VisualizedPriceInfo",
    version="1.0.0",
    description="None",
    author="YZK",
    author_email="thecourageyu@gmail.com",
    url="None",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    packages=[
        "VisualizedPriceInfo",
    ],
    install_requires=[
        "lxml",
        "matplotlib",
        "numpy",
        "pandas",
        "requests",
    ],
    #entry_points="""
    #[console_scripts]
    #powerline-shell=powerline_shell:main
    #""",
)