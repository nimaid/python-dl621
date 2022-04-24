# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='e621dl',
    version='0.1.0',
    description="A simple library to download e621 images with embedded tags',
    long_description=readme,
    author='Ella Jameson',
    author_email='ellagjameson@gmail.com',
    url='https://github.com/nimaid/python-e621dl',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'e621dl = e621dl.core:run',
        ]
    }
)

