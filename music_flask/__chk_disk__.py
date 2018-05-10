#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
  Python3 Music downloader

  Copyright (C) 2017 MAIBACH ALAIN

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  Contact: alain.maibach@gmail.com / 34 rue appienne, 13480 Calas - FRANCE.
'''

from __future__ import unicode_literals

import os
import sys
from collections import namedtuple

__author__ = "Alain Maibach"
__status__ = "Developement"

PYTHON3 = sys.version_info.major == 3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]

DiskNtuple = namedtuple('partition', 'device mountpoint fstype')
UsageNtuple = namedtuple('usage', 'total used free percent')

def convert_size_to_bytes(size):
    """ Convert size in Human Readable format to bytes """
    multipliers = {
        'kb': 1024,
        'mb': 1024*1024,
        'gb': 1024*1024*1024,
        'tb': 1024*1024*1024*1024
    }

    for suffix in multipliers:
        if size.lower().endswith(suffix):
            return int(size[0:-len(suffix)]) * multipliers[suffix]

        if size.lower().endswith('b'):
            return int(size[0:-1])

    try:
        return int(size)
    except ValueError: # for example "1024x"
        print('Malformed input!')
        exit()

def convert_bytes_to_size(num, suffix='o'):
    """Readable file size

    :param num: Bytes value
    :type num: int
    :param suffix: Unit suffix (optionnal) default = o
    :type suffix: str
    :rtype: str
    """

    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def disk_partitions(all_parts=False):
    """Return all mounted partitions as a nameduple.
    If all_parts == False return phyisical partitions only.
    """
    phydevs = []
    f_proc = open("/proc/filesystems", "r")
    for line in f_proc:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())

    retlist = []
    f_mtab = open('/etc/mtab', "r")
    for line in f_mtab:
        if not all_parts and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all_parts and fstype not in phydevs:
            continue
        if device == 'none':
            device = ''
        ntuple = DiskNtuple(device, mountpoint, fstype)
        retlist.append(ntuple)
    return retlist

def disk_usage(path):
    """Return disk usage associated with path."""
    status = os.statvfs(path)
    free = (status.f_bavail * status.f_frsize)
    total = (status.f_blocks * status.f_frsize)
    used = (status.f_blocks - status.f_bfree) * status.f_frsize
    try:
        #percent = ret = (float(used) / total) * 100
        percent = (float(used) / total) * 100
    except ZeroDivisionError:
        percent = 0
    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # http://goo.gl/sWGbH
    return UsageNtuple(total, used, free, round(percent, 1))

def path_freespace(fs_path):
    """ Return freespace of a file system directory """
    # unpacking disk_usage returned
    total, used, free, percent_used = disk_usage(fs_path)
    infos = {'used':used, 'total':total, 'free':free, 'percent_used':percent_used}

    percent = (free / total) * 100
    hr_fmt = convert_bytes_to_size(infos['free'])

    return {'bytes':infos['free'], 'percent':percent, 'human':hr_fmt}

def get_overall_infos():
    """ Return disk usage info for all system partitions """
    for part in disk_partitions():
        print(part)
        print("    %s\n" % str(disk_usage(part.mountpoint)))

if __name__ == '__main__':
    DIRECTORY = "/home/amaibach/Downloads/"
    FREE_SPACE = path_freespace(DIRECTORY)
    print(FREE_SPACE)
