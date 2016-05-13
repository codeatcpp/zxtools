#! /usr/bin/env python
# vim: set fileencoding=utf-8 :
""" TR-DOS diskette structure utils """

from collections import namedtuple

# TR-DOS diskette stucture description
#
# 0 track contains FAT in sectors 0..7
###############################################################################
# Each FAT record has the following format:
#
# 0                   1
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |FILENAME       |E| S | L |N|F|T|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# FILENAME  File name in ASCII
# E         File extension. Standard TR-DOS types are B, C, D, #.
# S         Depends on extension:
#               <B>: file size excluding variables
#               <C>: base address to load the code
# L         File size in bytes. This can be not accurate.
# N         File size in sectors.
# F         The number of the first sector with data.
# T         The number of the first tract with data.
#
FAT_RECORD_FMT = '<8sBHHBBB'
FATRecord = namedtuple('FATRecord', 'filename filetype start length '
                       'occupied_sectors first_sector first_track')

###############################################################################
#
# Sector 8 contains disk information in the following format:
#
#

