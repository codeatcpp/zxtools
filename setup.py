#! /usr/bin/env python
# vim: set fileencoding=utf-8 :

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    flicense = f.read()

setup(
    name='zxtools',
    version='0.0.2',
    description='Tools to manipulate files from Z80 Spectrum diskettes',
    long_description=readme,
    author='Kirill V. Lyadvinsky',
    author_email='mail@codeatcpp.com',
    download_url='https://github.com/codeatcpp/zxtools',
    url='http://www.codeatcpp.com',
    license=flicense,
    packages=find_packages(exclude=('test', 'docs')),
    test_suite="test",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)

