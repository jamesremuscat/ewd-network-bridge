from bleak import BleakScanner
from dataclasses import dataclass

import asyncio
import struct

address = "c2:77:e6:6e:72:66"  # Pack 3's receiver
address = 'E1:CA:D0:2E:B6:71'  # Voc RF4


@dataclass
class EWDReceiver:
    frequency: int = None
    battery_runtime: int = None
    battery_percentage: int = None

    mute_lock: bool = False
    key_lock: bool = False
    link_is_up: bool = False
    peaking: bool = False
    mute: bool = False
    settings_being_changed: bool = False
    firmware_corrupt: bool = False
    live_tx_view: bool = False

    tx_device_id: int = None
    tx_capsule_type: int = None
    tx_power: int = None

    tx_phantom_power: bool = False
    tx_framing_mode: bool = False
    tx_battery_rechargeable: bool = False
    tx_batt_status: bool = False
    tx_peaking: bool = False
    tx_capsule_connected: bool = False

    tx_version: str = None
    rx_version: str = None

    def receive_monitoring_data(self, data):
        freq = struct.unpack_from('i', data, 6)
        self.frequency = freq[0]

        status_bitmask = data[10]
        self.mute_lock = (status_bitmask & 1) > 0
        self.key_lock = (status_bitmask & 2) > 0
        self.link_is_up = (status_bitmask & 4) > 0
        self.peaking = (status_bitmask & 8) > 0
        self.mute = (status_bitmask & 16) > 0
        self.settings_being_changed = (status_bitmask & 32) > 0
        self.firmware_corrupt = (status_bitmask & 64) > 0
        self.live_tx_view = (status_bitmask & 128) > 0

        tx_device = struct.unpack_from('BBB', data, 11)
        self.tx_device_id = tx_device[0]
        self.tx_capsule_type = tx_device[1]
        self.tx_power = tx_device[2]

        batt_level = struct.unpack_from('B', data, 14)
        if batt_level[0] != 0x7F:
            self.battery_percentage = batt_level[0]
        else:
            self.battery_percentage = None

        batt_time = struct.unpack_from('H', data, 15)
        if batt_time[0] != 0x0FFF:
            self.battery_runtime = batt_time[0]
        else:
            self.battery_runtime = None

        tx_status = data[17]
        self.tx_phantom_power = (tx_status & 1) > 0
        self.tx_framing_mode = (tx_status & 2) > 0
        self.tx_battery_rechargeable = (tx_status & 4) > 0
        self.tx_batt_status = (tx_status & 8) > 0
        self.tx_peaking = (tx_status & 16) > 0
        self.tx_capsule_connected = (tx_status & 32) > 0

    def receive_version_data(self, data):
        rx_version = struct.unpack_from('BBB', data, 0)
        self.rx_version = '.'.join(map(lambda v: str(v), rx_version))
        tx_version = struct.unpack_from('BBB', data, 3)
        self.tx_version = '.'.join(map(lambda v: str(v), tx_version))


async def main():

    stop_event = asyncio.Event()

    my_device = EWDReceiver()

    def handle_data(device, advertising_data):
        if device.address.upper() == address.upper():
            mfr_data = advertising_data.manufacturer_data.get(1172)
            if mfr_data is not None:
                if len(mfr_data) == 18:
                    my_device.receive_monitoring_data(mfr_data)
                elif len(mfr_data) == 6:
                    my_device.receive_version_data(mfr_data)
                print(my_device)

    async with BleakScanner(handle_data) as scanner:
        ...
        # Important! Wait for an event to trigger stop, otherwise scanner
        # will stop immediately.
        await stop_event.wait()


if __name__ == '__main__':
    asyncio.run(main())
