#!.env/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import binascii

# client vars
host = '0.0.0.0'
port = 9060

# create socket
try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket Created: {}'.format(s))

    try:
        remote_ip = socket.gethostbyname(host)

        # Connect to remote server
        s.connect((remote_ip, port))

        print('Socket Connected to {} on IP: {}:{}'.format(host, remote_ip, port))

        msg = b"\x05\x01\x84\x08\x00\x1az\x08a\x07P'\x89\x17a\x08{\x00\x01\x8c\x00\x00\x00\x84\x026\tp(%\tp($\tp($\tp($\tp($\tp($\tp($\tp($\tp($\x08p($\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe5\xaf".hex()

        # Send some data to remote server
        message = msg.encode('utf-8')

        try:
            # Send the whole string
            s.sendall(bytes.fromhex(msg))
            print('Message: {} was sent successfully...'.format(msg))

            # Close the socket
            s.close()

        except socket.error as err:
            # Send failed
            print('Send failed for {}'.format(str(err)))
            sys.exit()

    except socket.gaierror as err:
        # could not resolve address
        print('Socket Error: {}'.format(str(err)))
        sys.exit()

except socket.error as err:
    print('The socket returned error {}'.format(str(err)))
    sys.exit()

