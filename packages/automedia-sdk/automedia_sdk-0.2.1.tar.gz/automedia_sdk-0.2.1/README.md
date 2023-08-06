# Automedia Python SDK

A basic SDK for interacting with an Automedia server.

## Installation

You can install the package from PyP:

```
$ pip3 install automedia_sdk
```

## Usage

Automedia's SDK for Python has a CLI.

```
$ automedia-cli --help
usage: automedia-cli [-r COMMAND [COMMAND ...]] [-o FILE_PATH] [--rpc-host <HOST>] [--rpc-port <PORT>]
                     [--rpc-user <USER>] [--rpc-password <PASSWORD>] [-h] [--version]

Launch Automedia CLI.

options:
  -r COMMAND [COMMAND ...], --run COMMAND [COMMAND ...]
                        run a command towards the endpoint.
  -o FILE_PATH, --open FILE_PATH
                        open file.

Automedia connection arguments:
  Setting the Automedia connection arguments.

  --rpc-host <HOST>     the host of the JSON RPC Automedia endpoint.
  --rpc-port <PORT>     the port of the JSON RPC Automedia endpoint.
  --rpc-user <USER>     the username for the JSON RPC Automedia endpoint.
  --rpc-password <PASSWORD>
                        the password for the JSON RPC Automedia endpoint.

About this package:
  Get additional information about this package.

  -h, --help            shows this help and exits.
  --version             shows the version of this package and exits.
```

However, most of the times you will be using it as a library:

```
import json
from automedia_sdk.api import AutomediaAPI
api = AutomediaAPI(
    "localhost",
    11321,
    "automedia",
    "automedia"
)
response = api.info()
print(json.dumps(response, indent=2))
```
