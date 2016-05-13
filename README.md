# Tools to manipulate files from Z80 Spectrum diskettes #

Here's a set of utils to manipulate files that were copied from TR-DOS diskettes. The tools were written to simplify the following workflow:

1. Grab diskette image using Hobbeta tool.
2. Strip the file header.
3. Convert resulting Zeus Z80 file to the plain text format.

It's very easy to use. Download the package, run `setup.py`, invoke in the following way:
```
$ python -m zxtools.hobeta strip input.hobetta result.zeus
$ python -m zxtools.zeus2txt result.zeus listing.txt
```
