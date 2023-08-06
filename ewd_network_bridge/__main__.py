
from .ewd import EWDReceiver
from .server import serve

import asyncio
import os

MAC_ADDRESS_ENV_VAR = 'EWD_MAC_ADDRESS'


def main():
    print('Starting EW-D bridge')
    device_mac = os.environ.get(MAC_ADDRESS_ENV_VAR)

    if device_mac is None:
        raise RuntimeError(f'{MAC_ADDRESS_ENV_VAR} must be specified!')

    my_device = EWDReceiver(device_mac)
    asyncio.run(serve(my_device))


if __name__ == '__main__':
    main()
