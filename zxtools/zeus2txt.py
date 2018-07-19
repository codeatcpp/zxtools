#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Kirill V. Lyadvinsky
# http://www.codeatcpp.com
#
# Licensed under the BSD 3-Clause license.
# See LICENSE file in the project root for full license information.
#
""" Convert Zeus Z80 assembler file to a plain text """

import argparse
import logging
import io

from zxtools import CHUNK_SIZE
from zxtools.common import default_main

CODE_ALIGN_WIDTH = 35


def show_info(*parsed_args):
    """Show some statistic about Zeus file"""
    # TODO Implement this function
    return parsed_args


def read_file(src_file):
    """Read source file for future processing"""
    with src_file:
        while True:
            chunk = src_file.read(CHUNK_SIZE)
            if chunk:
                for cur_char in chunk:
                    yield cur_char
            else:
                break


ASM_FIRST_TOKEN = 128
ASM_META = [
    "A", "ADC ", "ADD ", "AF'", "AF", "AND ", "B", "BC", "BIT ", "C",
    "CALL ", "CCF", "CP ", "CPD", "CPDR", "CPI", "CPIR", "CPL", "D", "DAA",
    "DE", "DEC ", "DEFB ", "DEFM ", "DEFS ", "DEFW ", "DI", "DISP ", "DJNZ ",
    "E", "EI", "ENT", "EQU ", "EX ", "EXX", "H", "HALT", "HL", "I", "IM ",
    "IN ", "INC ", "IND", "INDR", "INI", "INIR", "IX", "IY", "JP ", "JR ",
    "L", "LD ", "LDD", "LDDR", "LDI", "LDIR", "M", "NC", "NEG", "NOP", "NV",
    "NZ", "OR ", "ORG ", "OTDR", "OTIR", "OUT ", "OUTD", "OUTI", "P", "PE",
    "PO", "POP ", "PUSH ", "R", "RES ", "RET", "RETI", "RETN", "RL ", "RLA",
    "RLC ", "RLCA", "RLD", "RR ", "RRA", "RRC ", "RRCA", "RRD", "RST ",
    "SBC ", "SCF", "SET ", "SLA ", "SP", "SRA ", "SRL ", "SUB ", "V", "XOR ",
    "Z"]


def convert_file(parsed_args):
    """ Convert Zeus Z80 assembler file specified in zeus_file to the plain
    text and print it to the output_file """
    logger = logging.getLogger('convert_file')

    process_string = False
    strnum_lo = False, 0
    tab = False
    output = parsed_args.output_file
    strnum = 0
    cur_buffer = ""
    cur_line = io.StringIO()
    for cur_char in read_file(parsed_args.zeus_file):
        if process_string:
            cur_buffer += "0x%02X " % cur_char
            if not cur_char:  # End of string
                process_string = False
                strnum_lo = False, 0
                cur_str = cur_line.getvalue()
                print(cur_str, end="", file=output)
                if parsed_args.include_code:
                    print(" "*(CODE_ALIGN_WIDTH-len(cur_str))+";",
                          "0x%04X " % strnum + cur_buffer, file=output)
                else:
                    print(file=output)
                continue
            if tab:
                print(" "*cur_char, end="", file=cur_line)
                tab = False
                continue
            if cur_char == 0x0A:
                tab = True
                continue
            if cur_char < ASM_FIRST_TOKEN:  # Printable character
                print(chr(cur_char), end="", file=cur_line)
                continue
            try:
                print(ASM_META[cur_char-ASM_FIRST_TOKEN], end="", file=cur_line)
            except IndexError:
                logger.warning("Token not defined: 0x%02X (%d), at line %05d. "
                               "Skipped.", cur_char, cur_char, strnum)
        else:
            if not strnum_lo[0]:
                strnum_lo = True, cur_char
            else:
                strnum = strnum_lo[1] + cur_char*256
                if strnum == 0xFFFF:  # End of file
                    print(file=output)
                    break
                cur_line = io.StringIO()
                cur_line.truncate(0)
                cur_buffer = ""
                print("%05d" % strnum, end=" ", file=cur_line)
                process_string = True
    output.close()


def create_parser():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(
        description="Zeus Z80 assembler files converter")
    parser.add_argument(
        '-v', '--verbose', help="Increase output verbosity",
        action='store_true')

    subparsers = parser.add_subparsers(help="Available commands")
    subparsers.required = False

    info_parser = subparsers.add_parser(
        'info',
        help="Show information about the specified Zeus Z80 assembler file")
    info_parser.add_argument(
        'zeus_file', metavar='zeus-file', type=argparse.FileType('rb', 0),
        help="Input file with Zeus Z80 assembler (usually FILENAME.$C)")
    info_parser.set_defaults(func=show_info)

    convert_parser = subparsers.add_parser(
        'convert', help="Convert Zeus Z80 assembler file to a plain text file")
    convert_parser.add_argument(
        'zeus_file', metavar='zeus-file', type=argparse.FileType('rb', 0),
        help="Input file with Zeus Z80 assembler (usually FILENAME.$C)")
    convert_parser.add_argument(
        'output_file', metavar='output-file',
        type=argparse.FileType('w'), help="Path to the output file")
    convert_parser.add_argument(
        '--include-code', dest='include_code',
        action='store_true', help="Include original code in the output file")
    convert_parser.set_defaults(func=convert_file)

    return parser


def main():
    """Entry point"""
    default_main(create_parser())


if __name__ == '__main__':
    main()
