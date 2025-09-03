from __future__ import annotations

import argparse
import os

from dataclasses import dataclass, asdict, astuple
from enum import Enum, auto
from mmap import mmap
from struct import pack, unpack
from sys import exit


HEADER_MAGIC = 0x12345678
HEADER_RESERVED = 0x332255ff
HEADER_LENGTH = 20

PAYLOAD_BLOCK_1_LENGTH = 0x2ffe
PAYLOAD_BLOCK_2_LENGTH = 0x1000
PAYLOAD_BLOCK_3_LENGTH = lambda x: x - (PAYLOAD_BLOCK_1_LENGTH + PAYLOAD_BLOCK_2_LENGTH + HEADER_LENGTH)

FULL_PAYLOAD_BLOCK_1_OFFSET = 0x1002
FULL_PAYLOAD_BLOCK_2_OFFSET = 0x1c000
FULL_PAYLOAD_BLOCK_3_OFFSET = 0x1d000

UPDATE_PAYLOAD_BLOCK_1_OFFSET = HEADER_LENGTH
UPDATE_PAYLOAD_BLOCK_2_OFFSET = HEADER_LENGTH + PAYLOAD_BLOCK_1_LENGTH
UPDATE_PAYLOAD_BLOCK_3_OFFSET = HEADER_LENGTH + PAYLOAD_BLOCK_1_LENGTH + PAYLOAD_BLOCK_2_LENGTH


class FirmwareType(Enum):
    UNKNOWN = auto()
    FULL = auto()
    UPDATE = auto()


@dataclass(slots=True)
class Header:
    magic: int = HEADER_MAGIC
    length: int = 0
    header_sum: int = 0
    payload_sum: int = 0
    reserved: int = HEADER_RESERVED

    def __setattr__(self, name: str, value: object) -> None:
        if name == 'magic' and value != HEADER_MAGIC:
            raise ValueError('Invalid magic value')
        elif name == 'reserved' and value != HEADER_RESERVED:
            raise ValueError('Invalid reserved value')

        object.__setattr__(self, name, value)

        if all(hasattr(self, attr) for attr in self.__slots__) and \
           name in ('length', 'payload_sum'):
            object.__setattr__(self, 'header_sum', self.calc_sum())

    def __bytes__(self) -> bytes:
        return self.to_bytes()

    def __str__(self) -> str:
        return "\n".join(f"{key.replace('_', ' ')}: {value:08x}" for key, value in asdict(self).items())

    def to_bytes(self) -> bytes:
        return pack('>5I', *astuple(self))

    def calc_sum(self) -> int:
        buffer = bytearray(self.to_bytes())

        buffer[8:12] = bytearray(4)
 
        return sum(buffer)

    @property
    def dirty(self) -> bool:
        return self.header_sum != self.calc_sum()

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Header:
        if len(buffer) != HEADER_LENGTH:
            raise ValueError('Invalid header length')

        return cls(*unpack('>5I', buffer))


def main() -> None:
    parser = argparse.ArgumentParser(description='SWTG Firmware Checksum Calculator')
    parser.add_argument('-u', '--update', help='re-calculate sums', action='store_true')
    parser.add_argument('firmware', type=argparse.FileType('r+b'))

    args = parser.parse_args()

    print_or_exit = print if args.update else exit

    with args.firmware as f, mmap(f.fileno(), 0) as mm:
        binary = FirmwareType.UNKNOWN

        buffer = mm.read(2)

        match int.from_bytes(buffer, byteorder='little'):
            case 0x4000:
                binary = FirmwareType.FULL
            case 0x3412:
                buffer += mm.read(HEADER_LENGTH - 2)

                try:
                    header = Header.from_bytes(buffer)
                except Exception as e:
                    exit(e)

                binary = FirmwareType.UPDATE if (header.length + HEADER_LENGTH) == mm.size() else FirmwareType.UNKNOWN

        if binary is FirmwareType.UNKNOWN:
            exit('Invalid binary')

        offset, length = (FULL_PAYLOAD_BLOCK_1_OFFSET, PAYLOAD_BLOCK_1_LENGTH) if binary is FirmwareType.FULL else (UPDATE_PAYLOAD_BLOCK_1_OFFSET, PAYLOAD_BLOCK_1_LENGTH)

        mm.seek(offset, os.SEEK_SET)

        payload_sum = sum(mm.read(length))

        offset, length = (FULL_PAYLOAD_BLOCK_2_OFFSET, PAYLOAD_BLOCK_2_LENGTH) if binary is FirmwareType.FULL else (UPDATE_PAYLOAD_BLOCK_2_OFFSET, PAYLOAD_BLOCK_2_LENGTH)

        mm.seek(offset, os.SEEK_SET)

        payload_sum += sum(mm.read(length))

        offset = FULL_PAYLOAD_BLOCK_3_OFFSET if binary is FirmwareType.FULL else UPDATE_PAYLOAD_BLOCK_3_OFFSET

        mm.seek(offset, os.SEEK_SET)

        try:
            header = Header.from_bytes(mm.read(HEADER_LENGTH))
        except Exception as e:
            exit(e)

        payload_sum += 0xff * HEADER_LENGTH

        payload_sum += sum(mm.read(PAYLOAD_BLOCK_3_LENGTH(header.length)))

        if header.payload_sum != payload_sum:
            print_or_exit('Incorrect payload sum')

        print(header)

        if args.update:
            print('Updating checksums...')

            print('Old header: {}'.format(bytes(header).hex()))

            header.payload_sum = payload_sum # header sum will update as well

            print('New header: {}'.format(bytes(header).hex()))

            if binary is FirmwareType.UPDATE:
                mm[:HEADER_LENGTH] = bytes(header)

            mm[offset:offset + HEADER_LENGTH] = bytes(header)

    exit(0)

if __name__ == '__main__':
    main()
