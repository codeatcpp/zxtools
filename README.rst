=====================================
Tools to manipulate ZX Spectrum files
=====================================

.. image:: https://img.shields.io/travis/codeatcpp/zxtools/master.svg?style=flat
   :target: https://travis-ci.org/codeatcpp/zxtools

.. image:: https://codecov.io/gh/codeatcpp/zxtools/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/codeatcpp/zxtools

.. image:: https://img.shields.io/github/release/codeatcpp/zxtools.svg?style=flat
   :target: https://github.com/codeatcpp/zxtools/releases

.. image:: https://img.shields.io/pypi/v/zxtools.svg?style=flat
   :target: https://pypi.python.org/pypi/zxtools

.. image:: http://img.shields.io/pypi/dm/zxtools.svg?style=flat
   :target: https://pypi.python.org/pypi/zxtools

Here's a set of utils to manipulate files that were copied from a TR-DOS diskette or from a tape.

Originally the tools were written to simplify the following workflow:

1. Grab diskette image using `Hobeta <http://speccy.info/Hobeta>`_ tool.
2. Strip the file header and save the result to a new file.
3. Convert resulting `Zeus Z80 assembler <https://en.wikipedia.org/wiki/Zeus_Assembler>`_ file to the plain text format.

TODO: I have future plans to implement some more tools I need to restore my old ZX Spectrum projects.

But you can use them in the way you need. And it's very easy to use: download the package, run ``setup.py`` (or install via ``pip install zxtools``), invoke in the following way::

   $ python3 -m zxtools.hobeta strip input.hobeta result.zeus
   $ python3 -m zxtools.zeus2txt result.zeus listing.asm --include-code

.. image:: https://raw.githubusercontent.com/codeatcpp/zxtools/master/zeus2txt.jpg

NOTE: Python 3 is required to use this package, and Python 2 is not supported but you are welcome to fix it.

To view the resulting files with syntax colorization you can use special `Visual Studio Code plugin <https://marketplace.visualstudio.com/items?itemName=jia3ep.zeus-z80-asm>`_:

.. image:: https://raw.githubusercontent.com/codeatcpp/vscode-language-z80-asm/master/vscode.png
   :target: https://marketplace.visualstudio.com/items?itemName=jia3ep.zeus-z80-asm
