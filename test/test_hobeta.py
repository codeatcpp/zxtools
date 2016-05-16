#! /usr/bin/env python
# vim: set fileencoding=utf-8 :
""" hobeta.py tests """

import os
import io
import struct
import unittest
import tempfile
from collections import namedtuple
from zxtools import hobeta


class TestHobeta(unittest.TestCase):
    def test_ckechsum(self):
        data = b'F.load.AC\x00\x80\xf9\x06\x00\x07'
        self.assertEqual(hobeta.calc_checksum(data), 20661)

    def test_format_size(self):
        header_len = struct.calcsize(hobeta.HEADER_FMT)
        self.assertEqual(header_len, 17)

    def test_format(self):
        data = b"\x46\x2E\x6C\x6F\x61\x64\x2E\x41" \
               b"\x43\x00\x80\xF9\x06\x00\x07\xB5\x50"
        record = hobeta.Header._make(struct.unpack_from(hobeta.HEADER_FMT,
                                                        data))

        self.assertEqual(record.filename, b"F.load.A")
        self.assertEqual(record.filetype, ord('C'))
        self.assertEqual(record.start, 32768)
        self.assertEqual(record.length, 1785)
        self.assertEqual(record.first_sector, 0)
        self.assertEqual(record.occupied_sectors, 7)
        self.assertEqual(record.check_sum, 20661)

    def test_parse_info(self):
        test_file = io.BytesIO(b"\x46\x2E\x6C\x6F\x61\x64\x2E\x41"
                               b"\x43\x00\x80\xF9\x06\x00\x07\xB5"
                               b"\x50\x00\x00\x3B\x20\x4C\x4F\x41"
                               b"\x44\x45\x52\x20\x66\x6F\x72\x20")
        header, crc = hobeta.parse_info(test_file)

        self.assertEqual(header.filename, b"F.load.A")
        self.assertEqual(header.filetype, ord('C'))
        self.assertEqual(header.start, 32768)
        self.assertEqual(header.length, 1785)
        self.assertEqual(header.first_sector, 0)
        self.assertEqual(header.occupied_sectors, 7)
        self.assertEqual(header.check_sum, 20661)
        self.assertEqual(header.check_sum, crc)

    def test_parse_info2(self):
        test_file = io.BytesIO(b"\x46\x2E\x6C\x6F\x61\x64\x2E\x41"
                               b"\x43\x00\x80\x02\x00\x00\x07\xB5"
                               b"\x50\x00\x00\x3B\x20\x4C\x4F\x41"
                               b"\x44\x45\x52\x20\x66\x6F\x72\x20")
        header, crc = hobeta.parse_info(test_file)

        self.assertEqual(header.filename, b"F.load.A")
        self.assertEqual(header.filetype, ord('C'))
        self.assertEqual(header.start, 32768)
        self.assertEqual(header.length, 2)
        self.assertEqual(header.first_sector, 0)
        self.assertEqual(header.occupied_sectors, 7)
        self.assertEqual(header.check_sum, 20661)
        self.assertNotEqual(header.check_sum, crc)

    @staticmethod
    def strip_header(test_input_file, ignore_header_info):
        temp_output_path = tempfile.mkstemp()[1]
        temp_output_file = open(temp_output_path, "wb")
        Args = namedtuple('Args', "hobeta_file output_file ignore_header")
        parsed_args = Args(test_input_file,
                           temp_output_file,
                           ignore_header_info)
        copied_bytes = hobeta.strip_header(parsed_args)

        return temp_output_path, copied_bytes

    def test_strip_header1(self):
        test_input_file = io.BytesIO(b"\x46\x2E\x6C\x6F\x61\x64\x2E\x41"
                                     b"\x43\x00\x80\xF9\x06\x00\x07\xB5"
                                     b"\x50\x00\x00\x3B\x20\x4C\x4F\x41"
                                     b"\x44\x45\x52\x20\x66\x6F\x72")
        temp_output_path, bytes_count = self.strip_header(
            test_input_file, True)

        temp_output_file = open(temp_output_path, "rb")
        temp_output_file.seek(0, os.SEEK_END)
        try:
            self.assertEqual(temp_output_file.tell(), 14)
            self.assertEqual(bytes_count, 14)
        finally:
            temp_output_file.close()
            os.remove(temp_output_path)

    def test_strip_header2(self):
        test_input_file = io.BytesIO(b"\x46\x2E\x6C\x6F\x61\x64\x2E\x41"
                                     b"\x43\x00\x80\xF9\x06\x00\x07\xB5"
                                     b"\x50\x00\x00\x3B\x20\x4C\x4F\x41"
                                     b"\x44\x45\x52\x20\x66\x6F\x72\x20\x20")
        temp_output_path, bytes_count = self.strip_header(
            test_input_file, False)

        temp_output_file = open(temp_output_path, "rb")
        temp_output_file.seek(0, os.SEEK_END)
        try:
            self.assertEqual(temp_output_file.tell(), 16)
            self.assertEqual(bytes_count, 16)
        finally:
            temp_output_file.close()
            os.remove(temp_output_path)

    def test_strip_header3(self):
        test_input_file = io.BytesIO(b"\x46\x2E\x6C\x6F\x61\x64\x2E\x41"
                                     b"\x43\x00\x80\x0A\x00\x00\x07\xB5"
                                     b"\x50\x00\x00\x3B\x20\x4C\x4F\x41"
                                     b"\x44\x45\x52\x20\x66\x6F\x72\x20")
        temp_output_path, bytes_count = self.strip_header(
            test_input_file, False)

        temp_output_file = open(temp_output_path, "rb")
        temp_output_file.seek(0, os.SEEK_END)
        try:
            self.assertEqual(temp_output_file.tell(), 10)
            self.assertEqual(bytes_count, 10)
        finally:
            temp_output_file.close()
            os.remove(temp_output_path)

    def test_args_parser(self):
        parser = hobeta.parse_args(['hobeta-help'])
        self.assertTrue(parser.func)


if __name__ == '__main__':
    unittest.main()
