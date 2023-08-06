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
import subprocess, platform
import webbrowser as wb

import automedia_sdk
from automedia_sdk.api import AutomediaAPI
import automedia_sdk.lib.utils as utils
import automedia_sdk.lib.cmd_parsers as parsers
import automedia_sdk.lib.fortunes as fortunes


class AutomediaCLI(cmd.Cmd):
    """Automedia CLI application to control the different utils in the framework

    The user can type 'help' at any time to find the available commands
    included in the framework.

    Attributes:
        api (AutomediaAPI): The AutomediaAPI driver.
        method_list (list): A list of the available methods.
        prompt (str): The prompt to show n the UI
        automedia_rpc_host (str):  The JSON RPC host.
        automedia_rpc_port (int): The JSON RPC port.
        automedia_rpc_user (str): The JSON RPC user.
        automedia_rpc_passwd (str): The JSON RPC password.
        mongodb_host (str): The MongoDB host.
        mongodb_port (int): The MongoDB port.
        _logger (Logger): The logger object to store errors and info.
    """
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

    prompt = utils.colorize('\nautomedia-cli > ', "BOLD")
    CMD_CAT_TEXT = 'Text processing utils'
    CMD_CAT_FILE = 'File processing utils'
    CMD_CAT_IMAGE = 'Image processing utils'
    CMD_CAT_METADATA = 'Metadata processing utils'
    CMD_CAT_UTILS = 'Utils'

    # ===========
    # Constructor
    # ===========
    def __init__(self, **kwargs):
        """Constructor

        The method will automatically try to recover the parameters which are
        required.

        Keyword args:
            rpc_host (str): The hostname of the Automedia backend.
            rpc_port (int): The port to be used. It is serialized to string.
            rpc_user (str): The user to be used in the connection.
            rpc_pass (str): The password to be used in the connection.
        """
        # Disable cmd2's consumption of command-line arguments
        self.allow_cli_args = False

        print(self.welcome)

        self._logger = logging.getLogger("Automedia-CLI")
        cmd.Cmd.__init__(self)
        if kwargs.get("rpc_host"):
            self.automedia_rpc_host = kwargs.get("rpc_host")
        else:
            self.automedia_rpc_host = self._ask_for_data(
                "RPC host [localhost]: ",
                auto_complete=True,
                default="localhost"
            )
        try:
            if kwargs.get("rpc_port"):
                self.automedia_rpc_port = str(kwargs.get("rpc_port"))
            else:
                self.automedia_rpc_port = str(int(self._ask_for_data(
                    "RPC port [11321]: ",
                    auto_complete=True,
                    default=11321
                )))
        except ValueError as _:
            print(utils.colorize("\nERROR.\n", "ERROR BOLD"))
            text = "It does not look like a valid port."
            print(utils.colorize(text, "ERROR"))
            sys.exit()

        if kwargs.get("rpc_user"):
            self.automedia_rpc_user = kwargs.get("rpc_user")
        else:
            self.automedia_rpc_user = self._ask_for_data(
                "RPC user: ",
                auto_complete=True,
                default=None
            )

        if kwargs.get("rpc_password"):
            self.automedia_rpc_passwd = kwargs.get("rpc_password")
        else:
            self.automedia_rpc_passwd = self._ask_for_data(
                "RPC password: ",
                auto_complete=True,
                default=None
            )

        try:
            # Create the API
            self.api = AutomediaAPI(
                self.automedia_rpc_host,
                self.automedia_rpc_port,
                self.automedia_rpc_user,
                self.automedia_rpc_passwd,
                logger=self._logger
            )
            command = kwargs.get("command")
            if command:
                if len(command) > 1:
                    resp = getattr(self.api, command[0])(*command[1:])
                else:
                    resp = getattr(self.api, command[0])()

                if not resp["error"]:
                    print(textwrap.dedent(str(resp["result"])))
                else:
                    print(json.dumps(resp, indent=2))
                sys.exit()
            # Get method list from the help
            self.method_list = [
                "delete_data_from_proof",
                "delete_data_from_tx",
                "get_data_from_proof",
                "get_data_from_tx",
                "get_proof_from_tx",
                "hash",
                "help",
                "info",
                "moor_data",
                "moor_list",
                "use_blockchain",
                "verify_merkle_proof"
            ]
        except ConnectionRefusedError as _:
            print(utils.colorize("\nERROR.\n", "ERROR BOLD"))
            text = "Connection refused."
            print(utils.colorize(text, "ERROR"))
            sys.exit(1)

        # Remove cmd2 extra parameters
        del cmd.Cmd.do_alias
        del cmd.Cmd.do_edit
        # del cmd.Cmd.do_load
        # del cmd.Cmd.do_pyscript
        # del cmd.Cmd.run_pyscript
        # del cmd.Cmd.run_script
        del cmd.Cmd.do_shortcuts

    # Decorators
    # ----------
    def _output_decorator(method):
        """Decorator in charge of pretty printing the output

        It prints in red errors, in green successful executions and in yellow
        warnings and non-blocking errors.

        Args:
            method (callable): Any method of this class.
        """
        def magic(self, *args):
            try:
                response = method(self, *args)
                try:
                    if not response.get("error"):
                        print(utils.colorize("\nOK.\n", "SUCCESS BOLD"))
                        if isinstance(response["result"], (dict, list)):
                            text = json.dumps(response["result"], indent=2)
                        else:
                            text = response["result"]
                        print(utils.colorize(text, "SUCCESS"))
                    else:
                        print(utils.colorize("\nERROR.\n", "ERROR BOLD"))
                        text = json.dumps(response, indent=2)
                        print(utils.colorize(text, "ERROR"))
                except IndexError as _:
                    print(utils.colorize("\nWARNING.\n", "WARNING BOLD"))
                    print(utils.colorize("No command provided.", "WARNING"))
                except AttributeError as _:
                    print(utils.colorize("\nOK.\n", "SUCCESS BOLD"))
                    print(utils.colorize(response, "SUCCESS"))
            except Exception as err:
                print(utils.colorize("\nERROR.\n", "ERROR BOLD"))
                print(utils.colorize(str(err), "ERROR"))
        return magic

    # Other protected methods
    # -----------------------
    def _ask_for_data(self, message, auto_complete=True, default=None):
        """Method that asks for user input

        This method is usually called to request additional information like
        user, password, hosts or password. The method permits to define
        whether the value can be auto completed using default values.

        Args:
            message (str): Message to print in the prompt.
            auto_complete (bool): Whether it is autocompletable if blank.
            default (object): The default value if autocompleted is provided.
        """
        try:
            while True:
                answer = input(f"\t{message}")
                if answer:
                    return answer
                if auto_complete:
                    return default
                print(utils.colorize("\nWARNING.\n", "WARNING BOLD"))
                text = "This option cannot be empty. Please, try again."
                print(utils.colorize(text, "WARNING"))
        except KeyboardInterrupt as _:
            print("\n\nManually stopped by the user. Exiting…\n")
            sys.exit()

    # Standard CMD methods
    # --------------------
    @cmd.with_category(CMD_CAT_UTILS)
    @cmd.with_argparser(parsers.infoParser)
    @_output_decorator
    def do_info(self, args):
        """Prints information about the remote endpoints."""
        return self.api.info()

    @cmd.with_category(CMD_CAT_UTILS)
    @cmd.with_argparser(parsers.methodsParser)
    @_output_decorator
    def do_methods(self, method=None):
        """Get commands

        List commands.
        """
        return self.api.help()
        if method:
            return self.api.help(method)
        return self.api.help()

    @cmd.with_category(CMD_CAT_UTILS)
    @cmd.with_argparser(parsers.getFileParser)
    @_output_decorator
    def do_open_file(self, file_path):
        """Open file

        List commands.
        """
        content = self.api.get_file(file_path)
        print(content)
        print(f"data:*/*;base64,{content['result']}")
        wb.open(f"data:*/*;base64,{content}")
        # if platform.system() == 'Darwin':       # macOS
        #     subprocess.call(('open', filepath))
        # elif platform.system() == 'Windows':    # Windows
        #     os.startfile(filepath)
        # else:                                   # linux variants
        #     subprocess.call(('xdg-open', filepath))
        
        

    # @cmd.with_category(CMD_CAT_CONVENTIONAL_STORAGE)
    # @cmd.with_argparser(parsers.deleteDataParser)
    # @_output_decorator
    # def do_delete_data_from_tx(self, args):
    #     """Delete data found linked to a transaction."""
    #     return self.api.delete_data_from_tx(args.txid)


    # @cmd.with_category(CMD_CAT_CONVENTIONAL_STORAGE)
    # @cmd.with_argparser(parsers.deleteDataParser)
    # @_output_decorator
    # def do_delete_data_from_tx(self, args):
    #     """Delete data found linked to a transaction."""
    #     return self.api.delete_data_from_tx(args.txid)

    # @cmd.with_category(CMD_CAT_CONVENTIONAL_STORAGE)
    # @cmd.with_argparser(parsers.getDataParser)
    # @_output_decorator
    # def do_get_data_from_tx(self, args):
    #     """Get data found linked to a transaction.

    #     It can be either a string representing a hash or a Merkle proof. Then,
    #     It will query the MongoDB instance to collect the data whose
    #     information has been moored in the tx provided.
    #     """
    #     return self.api.get_data_from_tx(args.txid)

    # @cmd.with_category(CMD_CAT_BLOCKCHAIN)
    # @cmd.with_argparser(parsers.getProofParser)
    # @_output_decorator
    # def do_get_proof_from_tx(self, args):
    #     """Get proof found in a transaction.

    #     Note that this operation will get only the proof, not the raw tx
    #     itself. If the latter was desired, the operation needs to be performed
    #     using the 'use_blockchain' API.

    #     """
    #     return self.api.get_proof_from_tx(args.txid)

    # @cmd.with_category(CMD_CAT_BLOCKCHAIN)
    # @cmd.with_argparser(parsers.moorParser)
    # @_output_decorator
    # def do_moor_data(self, args):
    #     """Moor data in the blockchain.

    #     The application will automatically hash the information and try to moor
    #     it into the blockchain technology provided. The result returned will
    #     include a reference to the txid in which the data has been stored.

    #     There is a chance of adding  two special flags by explicitly stating
    #     `raw_data` or `no_store` to moor the data provided itself in the
    #     blockchain or to prevent Automedia from storing the information in its
    #     local conventional DB.

    #     Note that JSON objects should be quoted.
    #     """
    #     try:
    #         if args.info[0] in ("'", '"'):
    #             args.info = args.info[1:-1]
    #         data = json.loads(args.info)
    #     except json.JSONDecodeError as _:
    #         data = args.info
    #         print(
    #             utils.colorize("WARNING. ", "WARNING BOLD") +
    #             utils.colorize(
    #                 f"The data {data} is NOT a JSON object. It will be "
    #                 "process as a string.",
    #                 "WARNING"
    #             )
    #         )

    #     extra_params = {
    #         "raw_data": args.raw_data,
    #         "automedia_store": not args.no_store
    #     }

    #     return self.api.moor_data(data, **extra_params)

    # @cmd.with_category(CMD_CAT_BLOCKCHAIN)
    # @cmd.with_argparser(parsers.moorListParser)
    # @_output_decorator
    # def do_moor_list(self, args):
    #     """Moor a list of objects in the blockchain using a Merkle Tree

    #     The application will automatically hash the information and try to moor
    #     it into the blockchain technology provided. The result returned will
    #     include a reference to the txid as well as the proofs for the provided
    #     items.

    #     There is a chance of adding a special flag by explicitly stating
    #     `no_store` to moor the data provided itself in the blockchain or to
    #     prevent Automedia from storing the information in its local conventional
    #     DB.

    #     Note that the list should be quoted.
    #     """
    #     try:
    #         if args.info[0] in ("'", '"'):
    #             args.info = args.info[1:-1]
    #         data = json.loads(args.info)
    #     except json.JSONDecodeError as _:
    #         print(
    #             utils.colorize("WARNING. ", "WARNING BOLD") +
    #             utils.colorize(
    #                 f"The data {args.info} is NOT a JSON object."
    #             )
    #         )
    #         return

    #     extra_params = {
    #         "automedia_store": not args.no_store
    #     }

    #     return self.api.moor_list(data, **extra_params)

    # @cmd.with_category(CMD_CAT_BLOCKCHAIN)
    # @cmd.with_argparser(parsers.blockchainParser)
    # @_output_decorator
    # def do_use_blockchain(self, args):
    #     """Run a command towards a Automedia endpoint.

    #     Type 'use_blockchain' help to list all the commands. To get more
    #     information about each method type 'use_blockchain help<method_name>'.
    #     """
    #     return self.api.use_blockchain(
    #         args.command,
    #         *args.params
    #     )

    # @cmd.with_category(CMD_CAT_UTILS)
    # @cmd.with_argparser(parsers.verifyParser)
    # @_output_decorator
    # def do_verify_merkle_proof(self, args):
    #     """Verify a Merkle proof.

    #     The information SHOULD be a JSON quoted with single quotes.
    #     """
    #     # Prepare data
    #     if args.from_json:
    #         try:
    #             data = json.loads(args.from_json)
    #         except json.JSONDecodeError as _:
    #             print(utils.colorize("\nERROR.\n", "ERROR BOLD"))
    #             raise VerificationException(
    #                 f"The proof provided is NOT a JSON object."
    #             )
    #     elif args.from_file:
    #         with open(args.from_file) as input_file:
    #             data = json.loads(input_file.read())

    #     # Obtaining the data that will be moored inchain
    #     if isinstance(data, dict):
    #         if not data.get("header") or not data.get("body"):
    #             raise VerificationException(
    #                 "Verification failed. The proof does NOT have a correct "
    #                 "format."
    #             )
    #         merkle_proof = proof(from_dict=data)
    #         result = validate_proof(target_hash=args.merkle_root, proof=merkle_proof)
    #         if result:
    #             return "Verification successful. The proof provided " + \
    #                    f"belongs to Merkle root '{args.merkle_root}'."
    #         raise VerificationException(
    #             "Verification failed. The proof provided does NOT "
    #             f"belong to the Merkle root '{args.merkle_root}'."
    #         )
    #     raise VerificationException(
    #         "Verification failed. The proof provided does NOT "
    #         f"belong to the Merkle root '{args.merkle_root}'."
    #     )


def main():
    """Main function that starts the loop"""
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

    # Blockchain connection options
    automediaParser = parser.add_argument_group(
        'Automedia connection arguments',
        textwrap.fill('Setting the Automedia connection arguments.')
    )
    automediaParser.add_argument(
        '--rpc-host',
        metavar='<HOST>',
        action='store',
        default=None,
        help='the host of the JSON RPC Automedia endpoint.'
    )
    automediaParser.add_argument(
        '--rpc-port',
        metavar='<PORT>',
        action='store',
        type=int,
        default=None,
        help='the port of the JSON RPC Automedia endpoint.'
    )
    automediaParser.add_argument(
        '--rpc-user',
        metavar='<USER>',
        action='store',
        default=None,
        help='the username for the JSON RPC Automedia endpoint.'
    )
    automediaParser.add_argument(
        '--rpc-password',
        metavar='<PASSWORD>',
        action='store',
        default=None,
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

    cli = AutomediaCLI(
        rpc_host=args.rpc_host,
        rpc_port=args.rpc_port,
        rpc_user=args.rpc_user,
        rpc_password=args.rpc_password,
        command=args.run
    )
    cli.cmdloop()


if __name__ == '__main__':
    main()
