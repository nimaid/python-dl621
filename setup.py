# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()
    
setup(
    name='dl621',
    version='1.6.0',
    description='A simple python module and CLI utility to download e621 images with embedded XMP tags and description',
    long_description=readme,
    author='Ella Jameson',
    author_email='ellagjameson@gmail.com',
    url='https://github.com/nimaid/python-dl621',
    license=license,
    install_requires=["imgtag>=1.1.0", "requests>=2.27.1"],
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'dl621=dl621.core:run',
        ]
    }
)

