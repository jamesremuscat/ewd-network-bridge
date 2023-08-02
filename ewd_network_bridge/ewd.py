import asyncio
from bleak import BleakClient, BleakScanner

address = "c2:77:e6:6e:72:66"  # Pack 3's receiver

watched_characteristics = [
    30, 33, 42, 46, 48,
    53, 55, 57, 59, 61, 64, 67, 69, 71
]


async def get_values():
    values_by_handle = {}

    async with BleakClient(address, timeout=5) as client:
        for charHandle in watched_characteristics:
            val = await client.read_gatt_char(charHandle)
            values_by_handle[charHandle] = val

    return values_by_handle


async def main():
    prev_values = {}

    while True:
        new_values = await get_values()
        for handle, value in new_values.items():
            if prev_values.get(handle) != value:
                print(
                    f'[{handle}] {prev_values.get(handle)} => {value}'
                )
        prev_values = new_values
        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
