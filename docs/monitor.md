# Monitoring EW-D devices

The data displayed in the EW-D app in non-connected mode is found in the two
types of BLE advertisements broadcast by the receiver. Any Bluetooth receiver
can read this data, and no active connection to the EW-D device is necessary.

In both cases, the data is contained as a binary string in the
`manufacturer_data` section of the advertisements.

All data is represented little-endian.

## Version information

The shorter of the two advertisements contains the current version numbers of
the firmware running on the EW-D receiver and (when connected) transmitter.

Total length: 6 bytes

- Byte 0: Receiver major version
- Byte 1: Receiver minor version
- Byte 2: Receiver patch version
- Byte 3: Transmitter major version (or `0xFF` if no transmitter connected)
- Byte 4: Transmitter minor version (or `0xFF` if no transmitter connected)
- Byte 5: Transmitter patch version (or `0xFF` if no transmitter connected)

## Device state information

The longer (and less frequent - once every couple of seconds or so) of the
advertisements contains device state information. This is the information the
app can show you without actively making a connection to the receiver.

Total length: 18 bytes

- Byte 0 - 1: Seems to always be `0x02 0x03`
- Byte 2 - 5: ?
- Byte 6 - 9: Frequency in kHz (unsigned 4-byte integer)
- Byte 10: Receiver status bitmask
  - 1: Mute lock enabled
  - 2: Receiver panel keypad lock enabled
  - 4: Connected to transmitter
  - 8: AF peaking (at moment of broadcast)
  - 16: Muted
  - 32: Settings are being changed on the receiver panel
  - 64: Firmware is corrupt
  - 128: "Live TX view" (briefly true when transmitter first connects)
- Byte 11: Transmitter device ID
- Byte 12: Transmitter capsule type
- Byte 13: Transmitter power (factory rating - NOT RF signal strength)
- Byte 14: Tx battery percentage (or `0x7F` if no transmitter connected)
- Byte 15 - 16: Tx battery runtime estimate in minutes (unsigned 2-byte integer)
- Byte 17: Transmitter status bitmask
  - 1: Phantom power
  - 2: Framing mode (whatever that is)
  - 4: Battery is rechargeable (or possibly, is the Sennheiser pack)
  - 8: Battery status (low battery warning?)
  - 16: AF peaking
  - 32: Capsule is connected

## Limitations

Not included in this data are potentially useful things such as:

- Device name (requires active connection to device)
- RF signal level (not available?)
- AF signal level (not available?)
