# EW-D Network Bridge

## Project goal

The aim of this project is to provide an interface between a
[Sennheiser EW-D](https://en-uk.sennheiser.com/ew-d) Bluetooth connection and an ethernet network, to allow networked devices such
as dLive consoles to integrate with them in the same way as G4 (and presumably
EW-DX) receivers that have built-in Ethernet services.

This project is not in any way affiliated with Sennheiser.

## Project status

- Emulating a G4 receiver over Ethernet: done
- Reading data from EW-D receiver: done
- Writing data to EW-D receiver: Low priority

## Requirements

- A Linux host running BlueZ stack and Bluetooth LE-compatible adapter
  - If you're running recent Ubuntu/Debian with recent-ish hardware you're
    probably fine
- Git, Docker and `docker-compose` installed
- The EW-D receivers need to have been paired with an **Android** device before
  use (see limitations below)

## Finding EW-D devices

```bash
python -m ewd_network_bridge.scanner [timeout, default=60]
```

will scan nearby Bluetooth devices and list the MAC address and RF frequency of
any EW-D receivers found.

## Running a single instance

```bash
EWD_NAME="Vocal 1" EWD_MAC_ADDRESS="AB:CD:EF:01:23:45" python -m ewd_network_bridge
```

## Deployment

You probably have more than one EW-D receiver that you want to connect up. The
protocol requires one IP address per receiver, so the easiest way to run
multiple bridges on one machine is by using Docker and `docker-compose`.

- Check out this repository
- Edit the sample `docker-compose.yml` file to match your environment:
  - Change the `driver_opts: parent:` to match the name of the network interface
    on the host (this might be `eth0` or `en...` for a wired network adapter)
  - Change the `subnet` and `gateway` to match your network environment
  - Duplicate the `receiver_1` block until you have one for each of your EW-D
    receivers
  - Give each a unique name (`receiver_2`, ... or something more adventurous),
    IP address, and EW-D name and Bluetooth
    MAC address. [**TODO** make it easy to discover these]
  - Run `docker-compose up -d` to start the bridges.

Eventually the Docker image ought to be made available on Docker Hub, so you'll
not need to check out the repo first, and instead just work from the template
`docker-compose.yml`.

## Limitations

- Each receiver needs a unique IP address in order for the consoles to connect.
  Docker is used to simplify this deployment on a single host computer.
  - As a side-effect of using Docker in this way:
    - IP addresses must be manually assigned to each bridge
    - The host machine will **not** be able to access any of the bridges. This
      means that you can't run a `ping` from the host to check if things are
      working - you need to use a different machine on the same network.
- Changing settings on the EW-D is not currently supported.
- Obtaining some configuration settings (including receiver name) is only
  possible via an active Bluetooth connection and is not currently supported.
- Timeout values for the `Push` command are not supported; `Push` will always
  be responded to in the same way regardless of the parameter values passed with
  it, and clients must poll to receive updated data. (This is compatible with
  the way that Allen & Heath dLive consoles interoperate with Sennheiser G4s.)
- Receviers need to have been paired with an Android device (not an Apple device)
  since, for some reason, they don't broadcast this information once paired with
  anything fruity. (Needs further investigation into the pairing protocol.)

## References

- [Sennheiser documentation on Media Control Prototol](https://assets.sennheiser.com/global-downloads/file/12478/TI_1254_MetroMediensteuerung_ewG4_EN.pdf)
