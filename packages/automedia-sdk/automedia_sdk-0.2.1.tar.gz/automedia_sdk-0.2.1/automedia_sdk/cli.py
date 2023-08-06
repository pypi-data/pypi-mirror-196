###############################################################################
#
#    Copyright 2023 @ Félix Brezo (@febrezo)
#
#   Automedia is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


# Example based on json-rpc implementation for Savoir:
#   https://raw.githubusercontent.com/DXMarkets/Savoir/master/Savoir/Savoir.py

import argparse
import base64
import cmd2 as cmd
import json
import logging
import os
import random
import sys
import textwrap
import tempfile
import subprocess, platform
import webbrowser as wb

import automedia_sdk
from automedia_sdk.api import AutomediaAPI
import automedia_sdk.core.utils as utils
import automedia_sdk.core.fortunes as fortunes


def main():
    """Main function that starts the loop"""
    banner = """
                    _         _                           _ _       
                   / \  _   _| |_ ___  _ __ ___   ___  __| (_) __ _ 
                  / _ \| | | | __/ _ \| '_ ` _ \ / _ \/ _` | |/ _` |
                 / ___ \ |_| | || (_) | | | | | |  __/ (_| | | (_| |
                /_/   \_\__,_|\__\___/|_| |_| |_|\___|\__,_|_|\__,_|
                                                                
    """

    welcome = f"""

{utils.colorize(banner, "INFO BOLD")}

                        Coded with {utils.colorize("♥", "ERROR")} by """
    welcome += f"""{utils.colorize("Félix Brezo", "SUCCESS BOLD")}


Automedia CLI is a terminal User Interface to interact with the different elements
present in a Automedia network.

To get additional information about the available commands type """
    welcome += f"""'{utils.colorize("help", "BOLD")}'.

{utils.colorize(random.choice(fortunes.messages).center(80), "WARNING")}"""


    parser = argparse.ArgumentParser(
        description='Launch Automedia CLI.',
        add_help=False
    )
    parser.add_argument(
        '-r', '--run',
        metavar='COMMAND',
        nargs="+",
        required=False,
        help='run a command towards the endpoint.'
    )
    parser.add_argument(
        '-o', '--open',
        metavar='FILE_PATH',
        required=False,
        help='open file.'
    )

    # Blockchain connection options
    automediaParser = parser.add_argument_group(
        'Automedia connection arguments',
        textwrap.fill('Setting the Automedia connection arguments.')
    )
    automediaParser.add_argument(
        '--rpc-host',
        metavar='<HOST>',
        action='store',
        default="localhost",
        help='the host of the JSON RPC Automedia endpoint.'
    )
    automediaParser.add_argument(
        '--rpc-port',
        metavar='<PORT>',
        action='store',
        type=int,
        default=11321,
        help='the port of the JSON RPC Automedia endpoint.'
    )
    automediaParser.add_argument(
        '--rpc-user',
        metavar='<USER>',
        action='store',
        default="automedia",
        help='the username for the JSON RPC Automedia endpoint.'
    )
    automediaParser.add_argument(
        '--rpc-password',
        metavar='<PASSWORD>',
        action='store',
        default="automedia",
        help='the password for the JSON RPC Automedia endpoint.'
    )

    # About options
    # -------------
    groupAbout = parser.add_argument_group(
        'About this package',
        'Get additional information about this package.'
    )
    groupAbout.add_argument(
        '-h', '--help',
        action='help',
        help='shows this help and exits.'
    )
    groupAbout.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + automedia_sdk.__version__,
        help='shows the version of this package and exits.'
    )

    args = parser.parse_args()

    api = AutomediaAPI(
        args.rpc_host,
        args.rpc_port,
        args.rpc_user,
        args.rpc_password
    )

    if args.open:
        response = api.get_file(args.open)
        base64_bytes = response["result"].encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        temp_file_path = os.path.join(tempfile.gettempdir(), os.path.basename(args.open))
        with open(temp_file_path, "wb") as output_file:
            output_file.write(message_bytes)

        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', temp_file_path))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(temp_file_path)
        else:                                   # linux variants
            subprocess.call(('xdg-open', temp_file_path))
        
    elif args.run:
        print(f"Request > {args.run}")
        request = json.loads(args.run)
        response = getattr(api, request["method"])(*request["params"])
        print(json.dumps(response, indent=2, sort_keys=True))
    else:
        while True:
            request = json.loads(input("Request > "))
            response = getattr(api, request["method"])(*request["params"])
            print(json.dumps(response, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
