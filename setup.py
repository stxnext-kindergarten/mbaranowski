# -*- coding: utf-8 -*-
"""
Presence analyzer setup.
"""
import os
from setuptools import find_packages, setup


NAME = 'presence_analyzer'
VERSION = '0.1.0'


def read(*rnames):
    """
    Returns file's content.
    """
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name=NAME,
    version=VERSION,
    description='Presence analyzer',
    long_description=read('README.md'),
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Flask',
    ],
    entry_points='',
)
