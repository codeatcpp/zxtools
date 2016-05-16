#! /usr/bin/env python
# vim: set fileencoding=utf-8 :
""" trdos.py tests """

import unittest
import struct
from zxtools import trdos


class TestTRDos(unittest.TestCase):
    def test_fat_format(self):
        data = b"filenameC\x00\x80\xf9\x06\x07\xC1\x01"
        record = trdos.FATRecord._make(
            struct.unpack_from(trdos.FAT_RECORD_FMT, data))

        self.assertEqual(record.filename, b"filename")
        self.assertEqual(record.filetype, ord("C"))
        self.assertEqual(record.start, 32768)
        self.assertEqual(record.length, 1785)
        self.assertEqual(record.occupied_sectors, 0x07)
        self.assertEqual(record.first_sector, 0xC1)
        self.assertEqual(record.first_track, 0x01)


if __name__ == '__main__':
    unittest.main()
