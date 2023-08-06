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

from base64 import b64encode
import json
import logging
import automedia_sdk
import requests


from automedia_sdk import __version__


class AutomediaAPI(object):
    """Automedia official bindings for Python

    The Automedia object wraps an Automedia JSON RPC interface.

    Attributes:
        _rpchost (str): Automedia's RPC host.
        _rpcport (int): Automedia's RPC port.
        _rpcuser (str): Automedia's RPC username.
        _rpcpasswd (str): Automedia's RPC password.
        _auth_header (str): Authentication headers encoding RPC user and
            password.
        _logger (Logger): The logger instance to log the results.
        _base_url (string): The Base URL for the JSON RPC server.
        _rpc_call (str): Name of the method requested.
    """
    _id_count = 0

    def __init__(self, rpchost, rpcport, rpcuser=None, rpcpasswd=None,
                 rpc_call=None, **kwargs):
        """Constructor

        Args:
            rpchost (str): Automedia's RPC host.
            rpcport (int): Automedia's RPC port.
            rpcuser (str): Automedia's RPC username.
            rpcpasswd (str): Automedia's RPC password.
            rpc_call (str): Name of the method requested.
            **kwargs: Arbitrary keyword arguments such as `logger`.
        """
        self._logger = kwargs.get("logger", logging.getLogger("Automedia"))
        self._rpchost = rpchost
        self._rpcport = rpcport
        self._rpcuser = rpcuser
        self._rpcpasswd = rpcpasswd
        self._base_url = f"http://{self._rpchost}:{self._rpcport}"

        self._headers = {
            'Host': self._rpchost,
            'User-Agent': f'Automedia Python SDK v{__version__}',
            'content-type': 'application/json'
        }

        self._update_auth_header()

        self._rpc_call = rpc_call

    def __getattr__(self, name):
        # Omitting Python internal stuff
        if name.startswith('__') and name.endswith('__'):
            raise Exception("Automedia Python SDK Internal stuff.")

        return AutomediaAPI(
            self._rpchost,
            self._rpcport,
            self._rpcuser,
            self._rpcpasswd,
            rpc_call=name
        )

    def __call__(self, *args, **kwargs):
        """Callable for the object

        It automatically tracks the id of the petition and deals with the
        parameter management. Note that `moor_data` call will issue params
        as a JSON Object while the rest of the API calls will throw them as
        a list.
        """
        AutomediaAPI._id_count += 1

        if kwargs:
            params = kwargs
        else:
            params = args

        payload = {
            'jsonrpc': '2.0',
            'params': params,
            'method': self._rpc_call,
            'id': AutomediaAPI._id_count
        }

        try:
            resp = requests.post(
                self._base_url,
                data=json.dumps(payload, sort_keys=True),
                headers=self._headers
            )
        except Exception as exc:
            return {
                "result": None,
                "id": AutomediaAPI._id_count,
                "error": {
                    "code": 404,
                    "message": f"Connection error: \"{str(exc)}\"."
                }
            }

        if resp.status_code == 200:
            return resp.json()

        try:
            return resp.json()
        except Exception as _:
            return {
                "result": None,
                "id": AutomediaAPI._id_count,
                "error": {
                    "code": 500,
                    "message": resp.text
                }
            }

    def _update_auth_header(self):
        """Method that updates the authorization header

        It removes previous authorization in case of error.
        """
        if self._rpcuser and self._rpcpasswd:
            try:
                token = b64encode(
                    f'{self._rpcuser}:{self._rpcpasswd}'.encode()
                )
                self._headers["Authorization"] = f"Basic {token.decode()}"
            except TypeError as _:
                print()
                logging.warning(
                    "No valid credentials provided."
                    "Trying without an authentication header.",
                    "WARNING BOLD")
                self._headers.pop("Authorization", None)
