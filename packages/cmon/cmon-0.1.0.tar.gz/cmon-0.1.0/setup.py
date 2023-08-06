#!/usr/bin/env python
from setuptools import setup, find_packages

readme = open('./README.md', 'r')

setup(
    name='cmon',
    version='0.1.0',
    description='cmon is a utility that will monitor for any changes in your code and automatically restart them',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='nicriv',
    author_email='nicriv.dev@gmail.com',
    url='https://github.com/NicRiv/cmon',
    keywords=['utilities', 'testing', 'c', 'cpp', 'monitor'],
    license='MIT',
    packages=find_packages(),
    py_modules=['cmon'],
    install_requires=['click'],
    entry_points="""
    [console_scripts]
    cmon=cmon.cli:main
    """,
)