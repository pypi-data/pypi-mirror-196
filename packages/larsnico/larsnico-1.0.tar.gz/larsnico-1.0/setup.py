#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='larsnico',
    version='1.0',
    author='nicriv',
    packages=find_packages(),
    py_modules=['larsnico'],
    install_requires=[
        'click'
    ],
    entry_points="""
    [console_scripts]
    larsni=larsnico.main:main
    """
)