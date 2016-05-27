#! /usr/bin/env python
# vim: set fileencoding=utf-8 :
""" Convert Zeus Z80 assembler file to a plain text """

import argparse
import logging
import sys

from zxtools import CHUNK_SIZE


def show_info(*parsed_args):
    return


def read_file(src_file):
    with src_file:
        while True:
            chunk = src_file.read(CHUNK_SIZE)
            if chunk:
                for b in chunk:
                    yield b
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
    process_string = False
    strnum_lo = False, 0
    tab = False
    output = parsed_args.output_file
    strnum = 0
    for b in read_file(parsed_args.zeus_file):
        if process_string:
            if not b:  # End of string
                process_string = False
                strnum_lo = False, 0
                print(file=output)
                continue
            if tab:
                print(" "*b, end="", file=output)
                tab = False
                continue
            if b == 0x0A:
                tab = True
                continue
            if b < ASM_FIRST_TOKEN:  # Printable character
                print(chr(b), end="", file=output)
                continue
            try:
                print(ASM_META[b-ASM_FIRST_TOKEN], end="", file=output)
            except KeyError:
                print("Token not defined: 0x%02X (%d), at line %05d"
                      % (b, b, strnum))
        else:
            if not strnum_lo[0]:
                strnum_lo = True, b
            else:
                strnum = strnum_lo[1] + b*256
                if strnum == 0xFFFF:  # End of file
                    break
                print("%05d" % strnum, end=" ", file=output)
                process_string = True


def parse_args(args):
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(
        description="Zeus Z80 assembler files converter")
    parser.add_argument(
        '-v', '--verbose', help="Increase output verbosity",
        action='store_true')

    subparsers = parser.add_subparsers(help="Available commands")

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
    convert_parser.set_defaults(func=convert_file)

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
