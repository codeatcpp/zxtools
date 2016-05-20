#! /usr/bin/env python3
# vim: set fileencoding=utf-8 :

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='zxtools',
    version='1.0.15',
    description='Tools to manipulate files from ZX Spectrum',
    long_description=readme,
    author='Kirill V. Lyadvinsky',
    author_email='mail@codeatcpp.com',
    download_url='https://github.com/codeatcpp/zxtools',
    url='http://www.codeatcpp.com',
    license='BSD-3-Clause',
    packages=find_packages(exclude=('test', 'docs')),
    test_suite="test",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)

