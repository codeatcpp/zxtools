============================================
Python tools to manipulate ZX Spectrum files
============================================

Here's a set of utils to manipulate files that were copied from a TR-DOS diskette or from a tape.

Originally the tools were written to simplify the following workflow:

1. Grab diskette image using `Hobeta <http://speccy.info/Hobeta>`_ tool.
2. Strip the file header and save the result to a new file.
3. Convert resulting Zeus Z80 assembler file to the plain text format.

But you can use them in the way you need. And it's very easy to use: download the package, run ``setup.py`` (or install via ``pip install zxtools``), invoke in the following way::

   $ python3 -m zxtools.hobeta strip input.hobetta result.zeus
   $ python3 -m zxtools.zeus2txt result.zeus listing.txt

NOTE: You need Python 3 to use this package.
