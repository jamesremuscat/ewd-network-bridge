from bleak import BleakScanner

import asyncio
import struct
import sys


SENNHEISER_MANUFACTURER_ID = 1172


async def main(timeout=10):
    print('Scanning for EW-D receivers...')

    seen_addresses = []

    def handle_data(device, advertising_data):
        if device.address not in seen_addresses:
            if SENNHEISER_MANUFACTURER_ID in advertising_data.manufacturer_data:
                mfr_data = advertising_data.manufacturer_data[SENNHEISER_MANUFACTURER_ID]

                if len(mfr_data) == 18:
                    freq = struct.unpack_from('i', mfr_data, 6)[0] / 1000
                    print(f'{device.address}\t{advertising_data.local_name}\t{freq}')
            else:
                print(f'Not an EW-D receiver: {device.address}')

            seen_addresses.append(device.address)

    async with BleakScanner(handle_data):
        await asyncio.sleep(timeout)


if __name__ == '__main__':
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 10))
