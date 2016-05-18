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


ASM_META = {
    128:    "A",
    129:    "ADC ",
    130:    "ADD ",
    131:    "AF'",
    132:    "AF",
    133:    "AND ",
    134:    "B",
    135:    "BC",
    136:    "BIT ",
    137:    "C",
    138:    "CALL ",
    139:    "CCF",
    140:    "CP ",
    141:    "CPD",
    142:    "CPDR",
    143:    "CPI",
    144:    "CPIR",
    145:    "CPL",
    146:    "D",
    147:    "DAA",
    148:    "DE",
    149:    "DEC ",
    150:    "DEFB ",
    151:    "DEFM ",
    152:    "DEFS ",
    153:    "DEFW ",
    154:    "DI",
    155:    "DISP ",
    156:    "DJNZ ",
    157:    "E",
    158:    "EI",
    159:    "ENT",
    160:    "EQU ",
    161:    "EX ",
    162:    "EXX",
    163:    "H",
    164:    "HALT",
    165:    "HL",
    166:    "I",
    167:    "IM ",
    168:    "IN ",
    169:    "INC ",
    170:    "IND",
    171:    "INDR",
    172:    "INI",
    173:    "INIR",
    174:    "IX",
    175:    "IY",
    176:    "JP ",
    177:    "JR ",
    178:    "L",
    179:    "LD ",
    180:    "LDD",
    181:    "LDDR",
    182:    "LDI",
    183:    "LDIR",
    184:    "M",
    185:    "NC",
    186:    "NEG",
    187:    "NOP",
    188:    "NV",
    189:    "NZ",
    190:    "OR ",
    191:    "ORG ",
    192:    "OTDR",
    193:    "OTIR",
    194:    "OUT ",
    195:    "OUTD",
    196:    "OUTI",
    197:    "P",
    198:    "PE",
    199:    "PO",
    200:    "POP ",
    201:    "PUSH ",
    202:    "R",
    203:    "RES ",
    204:    "RET",
    205:    "RETI",
    206:    "RETN",
    207:    "RL ",
    208:    "RLA",
    209:    "RLC ",
    210:    "RLCA",
    211:    "RLD",
    212:    "RR ",
    213:    "RRA",
    214:    "RRC ",
    215:    "RRCA",
    216:    "RRD",
    217:    "RST ",
    218:    "SBC ",
    219:    "SCF",
    220:    "SET ",
    221:    "SLA ",
    222:    "SP",
    223:    "SRA ",
    224:    "SRL ",
    225:    "SUB ",
    226:    "V",
    227:    "XOR ",
    228:    "Z"
}


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
            if b < min(ASM_META, key=ASM_META.get):  # Printable character
                print(chr(b), end="", file=output)
                continue
            try:
                print(ASM_META[b], end="", file=output)
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
