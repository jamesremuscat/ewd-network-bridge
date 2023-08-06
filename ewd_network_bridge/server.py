import asyncio

from bleak import BleakScanner

from .protocol import MediaControlProtocol


MEDIA_CONTROL_SERVER_PORT = 53212


async def serve(ewd_device):
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: MediaControlProtocol(ewd_device),
        local_addr=('0.0.0.0', MEDIA_CONTROL_SERVER_PORT))

    ewd_device.start()

    while True:
        await asyncio.sleep(3600)
