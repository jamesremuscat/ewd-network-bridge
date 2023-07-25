
import asyncio
from .server import serve


def main():
    print('Starting EW-D bridge')
    asyncio.run(serve())


if __name__ == '__main__':
    main()
