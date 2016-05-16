#! /usr/bin/env python
# vim: set fileencoding=utf-8 :

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    flicense = f.read()

setup(
    name='zxtools',
    version='0.0.1',
    description='TR-DOS files utils',
    long_description=readme,
    author='Kirill V. Lyadvinsky',
    author_email='mail@codeatcpp.com',
    url='https://github.com/codeatcpp/zxtools',
    license=flicense,
    packages=find_packages(exclude=('test', 'docs')),
    test_suite="test"
)

