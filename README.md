# EW-D Network Bridge

## Project goal

The aim of this project is to provide an interface between a
[Sennheiser EW-D](https://en-uk.sennheiser.com/ew-d) Bluetooth connection and an ethernet network, to allow networked devices such
as dLive consoles to integrate with them in the same way as G4 (and presumably
EW-DX) receivers that have built-in Ethernet services.

This project is not in any way affiliated with Sennheiser.

## Project status

- Emulating a G4 receiver over Ethernet: done
- Reading data from EW-D receiver: In progress
- Writing data to EW-D receiver: Low priority

## Requirements

- A Linux host running BlueZ stack and Bluetooth LE-compatible adapter
  - If you're running recent Ubuntu/Debian with recent-ish hardware you're
    probably fine
- Git, Docker and `docker-compose` installed

## Deployment

- Check out this repository
- Edit the sample `docker-compose.yml` file to match your environment:
  - Change the `driver_opts: parent:` to match the name of the network interface
    on the host (this might be `eth0` or `en...` for a wired network adapter)
  - Change the `subnet` and `gateway` to match your network environment
  - Duplicate the `receiver_1` block until you have one for each of your EW-D
    receivers
  - Give each a unique name (`receiver_2`, ... or something more adventurous),
    IP address and EW-D Bluetooth
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
- The main priority is obtaining read-only data (battery life, RF and AF signal);
  changing settings on the EW-D is a secondary concern.
