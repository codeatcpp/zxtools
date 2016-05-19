#! /usr/bin/env python
# vim: set fileencoding=utf-8 :

from setuptools import setup, find_packages


with open('LICENSE') as f:
    flicense = f.read()

setup(
    name='zxtools',
    version='1.0.0',
    description='Tools to manipulate files from ZX Spectrum',
    long_description='Here’s a set of utils to manipulate files that were copied from a TR-DOS diskette or from a tape.'
    '\n\nYou can find more info in README.md at https://github.com/codeatcpp/zxtools',
    author='Kirill V. Lyadvinsky',
    author_email='mail@codeatcpp.com',
    download_url='https://github.com/codeatcpp/zxtools',
    url='http://www.codeatcpp.com',
    license=flicense,
    packages=find_packages(exclude=('test', 'docs')),
    test_suite="test",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)

