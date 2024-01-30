import argparse
import mmap
import os
import struct
import sys


HEADER_LENGTH = 20
HEADER_MAGIC = 0x12345678
PAYLOAD_LENGTH = 0x2ffe + 0x1000


def main() -> None:
    parser = argparse.ArgumentParser(description='SWTGW tool')
    parser.add_argument('-u', '--update', help='Re-calculate sums', action='store_true')
    parser.add_argument('infile', type=argparse.FileType('r+b'))

    args = parser.parse_args()

    print_or_exit = print if args.update else sys.exit

    with args.infile as in_file:
        with mmap.mmap(in_file.fileno(), 0) as in_map:
            header = bytearray(in_map.read(HEADER_LENGTH))
            magic, length, header_sum, payload_sum, reserved = struct.unpack('>5I', header)
            print(f"magic: {magic:08x}\n" \
                  f"length: {length:08x}\n" \
                  f"header sum: {header_sum:08x}\n" \
                  f"payload sum: {payload_sum:08x}\n" \
                  f"reserved: {reserved:08x}", header.hex(), sep='\n')
            if magic != HEADER_MAGIC:
                sys.exit('Invalid header magic')
            if length + HEADER_LENGTH != in_map.size():
                sys.exit('Invalid header file length')
            # Placeholder for the header sum
            header[8:12] = b'\x00' * 4
            if header_sum != sum(header):
                print_or_exit('Invalid header checksum')
            calc_sum = sum(in_map.read(PAYLOAD_LENGTH))
            # Skip payload header
            in_map.seek(HEADER_LENGTH, os.SEEK_CUR)
            # Placeholder for payload header sum
            calc_sum += 0xff * HEADER_LENGTH
            calc_sum += sum(in_map.read())
            if calc_sum != payload_sum:
                print_or_exit('Invalid payload checksum')
            if args.update:
                # Update the payload sum
                header[12:16] = struct.pack('>I', calc_sum)
                # Update the header sum
                calc_sum = sum(header)
                header[8:12] = struct.pack('>I', calc_sum)
                print(header.hex())
                # Update headers
                in_map[:HEADER_LENGTH] = header
                in_map[PAYLOAD_LENGTH+HEADER_LENGTH:PAYLOAD_LENGTH+HEADER_LENGTH*2] = header
    sys.exit(0)


if __name__ == '__main__':
    main()

