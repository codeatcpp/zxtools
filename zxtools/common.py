#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Kirill V. Lyadvinsky
# http://www.codeatcpp.com
# Licensed under the BSD 3-Clause license.
# See LICENSE file in the project root for full license information.
#
""" Common functions """

import sys
import logging


def safe_parse_args(parser, args):
    """Safely parse arguments"""
    try:
        options = parser.parse_args(args)
        if len(args) == 0:
            raise ValueError
    except ValueError:
        parser.print_help()
        sys.exit(0)

    return options


def default_main(parser):
    """ Default entry point implementation """
    args = safe_parse_args(parser, sys.argv[1:])
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if hasattr(args, 'func'):
        args.func(args)

    return args
