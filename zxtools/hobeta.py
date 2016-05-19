#! /usr/bin/env python
# vim: set fileencoding=utf-8 :
""" Hobeta file utils """

import os
import sys
import logging
import struct
from collections import namedtuple
import argparse

from zxtools import CHUNK_SIZE

HEADER_FMT = '<8sBHHBBH'
Header = namedtuple(
    'Header',
    'filename filetype start length first_sector occupied_sectors check_sum')


def hobeta_help(*parsed_args):
    print(
        "Hobeta file has the following format:\n"
        "(this is accroding to http://speccy.info/Hobeta)\n"
        "\n"
        "0                   1                   2                   3\n"
        "0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n"
        "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
        "|TR-DOS FILENAME|T| S | L |F|C|CHK| RAW FILE DATA...\n"
        "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
        "\n"
        " T   - File type. Standard types are B, C, D, #.\n"
        " S   - TR-DOS START parameter (ORG for CODE, LEN for BASIC)\n"
        " L   - TR-DOS LENGTH parameter (size in bytes)\n"
        " F   - The first occupied sector or just padding?\n"
        " C   - File size in TR-DOS sectors\n"
        " CHK - Checksum of this header (excluding CHK)")


def calc_checksum(data):
    """ Calculate checksum for data """
    check_sum = 0
    for i, value in enumerate(data):
        check_sum = (check_sum + value*257 + i) % 0x10000
    return check_sum


def parse_info(hobeta_file):
    """ Parse Hobeta header """
    logger = logging.getLogger('parse_info')

    header_len = struct.calcsize(HEADER_FMT)
    logger.debug(header_len)
    data = hobeta_file.read(header_len)

    actual_check_sum = calc_checksum(data[0:header_len-2])
    header = Header._make(struct.unpack_from(HEADER_FMT, data))
    logger.debug(header)

    return header, actual_check_sum


def show_info(parsed_args):
    """ Show info from Hobeta header """
    header, crc = parse_info(parsed_args.hobeta_file)

    print(
        ("File name:\t" + header.filename.decode("ascii") + "\n" +
         "Extension:\t" + chr(header.filetype) + "\n" +
         ("Prg LEN:\t" if header.filetype == ord('B') else "Place at:\t") +
         str(header.start) + "\n" +
         "File size:\t" + str(header.length) + "\n" +
         "First sector:\t" + str(header.first_sector) + "\n" +
         "Occupied sectors:\t" + str(header.occupied_sectors) + "\n" +
         "Check sum:\t" + str(header.check_sum) + " " +
         ("(OK)" if crc == header.check_sum
          else "(WRONG! Should be " + str(crc) + ")")).expandtabs(20))


def strip_header(parsed_args):
    """ Copy the source file to the output file excluding Hobeta header """
    logger = logging.getLogger('strip_header')

    header, crc = parse_info(parsed_args.hobeta_file)
    if header.check_sum != crc:
        print("WARNING: wrong checksum in the header.")

    header_size = struct.calcsize(HEADER_FMT)

    with parsed_args.hobeta_file as src_file:
        src_file.seek(0, os.SEEK_END)
        hobeta_file_size = src_file.tell()
        if parsed_args.ignore_header:
            bytes_to_copy = hobeta_file_size-header_size
        else:
            bytes_to_copy = header.length
        logger.debug(bytes_to_copy)

        length = bytes_to_copy
        src_file.seek(header_size)
        with parsed_args.output_file as dst_file:
            while length:
                chunk_size = min(CHUNK_SIZE, length)
                data = src_file.read(chunk_size)
                if not data:
                    break
                dst_file.write(data)
                length -= len(data)
    print("Created file %s, %d bytes copied." %
          (dst_file.name, bytes_to_copy-length))
    return bytes_to_copy-length


def parse_args(args):
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Hobeta files converter")
    parser.add_argument(
        '-v', '--verbose', help="Increase output verbosity",
        action='store_true')

    subparsers = parser.add_subparsers(help="Available commands")

    info_parser = subparsers.add_parser(
        'info',
        help="Show information about the specified Hobeta file")
    info_parser.add_argument(
        'hobeta_file', metavar='hobeta-file', type=argparse.FileType('rb', 0),
        help="Input file in Hobeta format (usually FILENAME.$C)")
    info_parser.set_defaults(func=show_info)

    strip_parser = subparsers.add_parser('strip', help="Strip Hobeta header")
    strip_parser.add_argument(
        'hobeta_file', metavar='hobeta-file', type=argparse.FileType('rb', 0),
        help="Input file in Hobeta format (usually FILENAME.$C)")
    strip_parser.add_argument(
        'output_file', metavar='output-file',
        type=argparse.FileType('wb', 0), help="Path to the output file")
    strip_parser.add_argument(
        '--ignore-header', dest='ignore_header',
        action='store_true', help="Ignore the file size from Hobeta header")
    strip_parser.set_defaults(func=strip_header)

    help_parser = subparsers.add_parser(
        'hobeta-help',
        help="Show Hobeta header format description")
    help_parser.set_defaults(func=hobeta_help)

    return parser.parse_args(args)


def main():
    """ Entry point """
    args = parse_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if hasattr(args, 'func'):
        args.func(args)


if __name__ == '__main__':
    main()
