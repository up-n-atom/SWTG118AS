import argparse
import mmap
import os
import struct
import sys


HEADER_LENGTH = 20
HEADER_MAGIC = 0x12345678
HEADER_RESERVED = 0x332255FF
PAYLOAD_LENGTH = 0x2ffe + 0x1000


def main() -> None:
    parser = argparse.ArgumentParser(description='SWTG Update Firmware Checksum Calculator')
    parser.add_argument('-u', '--update', help='Re-calculate sums', action='store_true')
    parser.add_argument('firmware', type=argparse.FileType('r+b'))

    args = parser.parse_args()

    print_or_exit = print if args.update else sys.exit

    with args.firmware as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            header = bytearray(mm.read(HEADER_LENGTH))

            magic, length, header_sum, payload_sum, reserved = struct.unpack('>5I', header)

            print(f"magic: {magic:08x}",
                  f"length: {length:08x}",
                  f"header sum: {header_sum:08x}",
                  f"payload sum: {payload_sum:08x}",
                  f"reserved: {reserved:08x}",
                  header.hex(), sep='\n')

            if magic != HEADER_MAGIC:
                sys.exit('Invalid header magic')

            if length + HEADER_LENGTH != mm.size():
                sys.exit('Invalid header file length')

            # Placeholder for the header sum
            header[8:12] = b'\x00' * 4

            if header_sum != sum(header):
                print_or_exit('Invalid header checksum')

            # Calculate payload sum...
            calc_sum = sum(mm.read(PAYLOAD_LENGTH))

            # Skip payload header
            mm.seek(HEADER_LENGTH, os.SEEK_CUR)

            # Placeholder for payload header sum
            calc_sum += 0xff * HEADER_LENGTH

            # Resume payload sum 
            calc_sum += sum(mm.read())

            if calc_sum != payload_sum:
                print_or_exit('Invalid payload checksum')

            if args.update:
                # Update the payload sum
                header[12:16] = struct.pack('>I', calc_sum)

                # Calculate the header sum
                calc_sum = sum(header)

                # Update the header sum
                header[8:12] = struct.pack('>I', calc_sum)

                print(header.hex())

                # Update headers
                mm[:HEADER_LENGTH] = header
                mm[PAYLOAD_LENGTH+HEADER_LENGTH:PAYLOAD_LENGTH+HEADER_LENGTH*2] = header

    sys.exit(0)


if __name__ == '__main__':
    main()

