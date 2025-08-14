import argparse
import os

from dataclasses import dataclass, field, asdict, astuple
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


class FileType(Enum):
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

    def __setattr__(self, name, value) -> None:
        if name == 'magic' and value != HEADER_MAGIC:
            raise AttributeError('Invalid magic value')
        elif name == 'reserved' and value != HEADER_RESERVED:
            raise AttributeError('Invalid reserved value')

        object.__setattr__(self, name, value)

        if all(hasattr(self, attr) for attr in self.__slots__) and \
           name in ('length', 'payload_sum'):
            object.__setattr__(self, 'header_sum', Header.calc_sum(self))

    def __bool__(self) -> bool:
        return Header.is_valid(self)

    def __bytes__(self) -> bytes:
        return Header.to_bytes(self)

    def __str__(self) -> str:
        return "magic: {:08x}\n" \
               "length: {:08x}\n" \
               "header sum: {:08x}\n" \
               "payload sum: {:08x}\n" \
               "reserved: {:08x}".format(*astuple(self))

    @staticmethod
    def calc_sum(header) -> None:
        buffer = bytearray(bytes(header))
        buffer[8:12] = bytearray(4)
        return sum(buffer)

    @staticmethod
    def is_valid(header, ignore_sum=True) -> bool:
        return header.magic == HEADER_MAGIC and \
               header.reserved == HEADER_RESERVED and \
               (ignore_sum or header.header_sum == Header.calc_sum(header))

    @staticmethod
    def to_bytes(header) -> bytes:
        return pack('>5I', *astuple(header))

    @staticmethod
    def from_bytes(buffer: bytes) -> None:
        return Header(*unpack('>5I', buffer))


def main() -> None:
    parser = argparse.ArgumentParser(description='SWTG Firmware Checksum Calculator')
    parser.add_argument('-u', '--update', help='re-calculate sums', action='store_true')
    parser.add_argument('firmware', type=argparse.FileType('r+b'))

    args = parser.parse_args()

    print_or_exit = print if args.update else exit

    with args.firmware as f, mmap(f.fileno(), 0) as mm:
        header = None
        match int.from_bytes(buffer := mm.read(2), byteorder='little'):
            case 0x4000:
                binary = FileType.FULL
            case 0x3412:
                buffer += mm.read(HEADER_LENGTH - 2)
                header = Header.from_bytes(buffer)
                binary = FileType.UPDATE if header and (header.length + HEADER_LENGTH) == mm.size() else FileType.UNKNOWN
            case _:
                exit('Invalid binary')

        if binary is FileType.UNKNOWN:
            exit('Invalid binary')

        offset, length = (FULL_PAYLOAD_BLOCK_1_OFFSET, PAYLOAD_BLOCK_1_LENGTH) if binary is FileType.FULL else (UPDATE_PAYLOAD_BLOCK_1_OFFSET, PAYLOAD_BLOCK_1_LENGTH)

        mm.seek(offset, os.SEEK_SET)

        payload_sum = sum(mm.read(length))

        offset, length = (FULL_PAYLOAD_BLOCK_2_OFFSET, PAYLOAD_BLOCK_2_LENGTH) if binary is FileType.FULL else (UPDATE_PAYLOAD_BLOCK_2_OFFSET, PAYLOAD_BLOCK_2_LENGTH)

        mm.seek(offset, os.SEEK_SET)

        payload_sum += sum(mm.read(length))

        offset = FULL_PAYLOAD_BLOCK_3_OFFSET if binary is FileType.FULL else UPDATE_PAYLOAD_BLOCK_3_OFFSET

        mm.seek(offset, os.SEEK_SET)

        header = Header.from_bytes(mm.read(HEADER_LENGTH))

        if not header:
            exit('Invalid binary')

        payload_sum += 0xff * HEADER_LENGTH

        payload_sum += sum(mm.read(PAYLOAD_BLOCK_3_LENGTH(header.length)))

        if header.payload_sum != payload_sum:
            print_or_exit('Incorrect payload sum')
        else:
            print(header)

        if args.update:
            print('Updating checksums...')

            print('Old header: {}'.format(bytes(header).hex()))

            header.payload_sum = payload_sum # header sum will update as well

            print('New header: {}'.format(bytes(header).hex()))

            if binary is FileType.UPDATE:
                mm[:HEADER_LENGTH] = bytes(header)

            mm[offset:offset + HEADER_LENGTH] = bytes(header)

    exit(0)

if __name__ == '__main__':
    main()
