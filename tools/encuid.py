#!/usr/bin/python3

import sys

try:
    from Crypto.Cipher import AES
except ImportError:
    from Cryptodome.Cipher import AES

LO_KEY = b'59494F4754fff00\0' # lower case
UP_KEY = b'59494F4754fff01\0' # upper case

if __name__ == "__main__":
    uid = b'10093f30'
    if len(sys.argv) > 1 and len(sys.argv[1]) == 8:
        uid = bytes(sys.argv[1].lower(), 'ascii')
    print('unique id:', uid.decode('ascii'))
    aes = AES.new(LO_KEY, AES.MODE_ECB)
    dat = aes.encrypt(uid + uid)
    print('encrypted uid str:', dat[:8].hex())
    print('encrypted uid hex:', dat[:8].hex().encode('ascii').hex())