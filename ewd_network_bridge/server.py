import asyncio

from bleak import BleakScanner

from .protocol import MediaControlProtocol


MEDIA_CONTROL_SERVER_PORT = 53212


async def serve():

    devices = await BleakScanner.discover(return_adv=True)
    for device in devices.values():
        print(device)

    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: MediaControlProtocol(),
        local_addr=('0.0.0.0', MEDIA_CONTROL_SERVER_PORT))

    while True:
        await asyncio.sleep(3600)
