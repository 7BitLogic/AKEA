# -*- coding: utf-8 -*-

# Learn something: https://github.com/.../setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Raoul-Amadeus Lorbeer',
    author_email='TBD',
    url='https://github.com/...',
    install_requires=[
          'qrcode',
          'pyzbar',
          'zbar',
          'python-opencv',
          'numpy',
          'pillow'
          ],
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

