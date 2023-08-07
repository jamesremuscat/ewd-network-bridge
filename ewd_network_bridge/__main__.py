
from .ewd import EWDReceiver
from .server import serve

import asyncio
import os

MAC_ADDRESS_ENV_VAR = 'EWD_MAC_ADDRESS'


def main():
    device_mac = os.environ.get(MAC_ADDRESS_ENV_VAR)

    if device_mac is None:
        raise RuntimeError(f'{MAC_ADDRESS_ENV_VAR} must be specified!')

    device_name = os.environ.get('EWD_NAME')

    print(f'Starting EW-D bridge for {device_name or "unnamed"} ({device_mac})')

    my_device = EWDReceiver(device_mac, device_name)
    asyncio.run(serve(my_device))


if __name__ == '__main__':
    main()
