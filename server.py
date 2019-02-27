#!.env/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
from db import db_session
from decoder import inspect_header, decode_header, decode_readings
from datetime import datetime
from models import Tx, TxHeader, TxReading
from sqlalchemy import exc


def main():
    """
    The main program for the Python Socket Server.
    Receive datastream.  Detect and Decode Header.
    Create data transmission readings in the database
    :return: data obj
    """

    while True:
        # wait
        print('Hi.  Please send me some data.')

        try:
            # accept the socket
            connection, client_address = s.accept()
            print('{} from client {}'.format(connection, client_address))

            # receive the data in small chunks
            while True:

                # our data obj in 1024 byte chunks
                data = connection.recv(1024)

                if data:
                    tx = data.hex()

                    # set the header values to determine the message type
                    header = inspect_header(tx[:34], 2)

                    # return decoded data as an ordered dictionary
                    decoded = decode_header(header)

                    # check to see if we have a decoded data object
                    if decoded:

                        # create a new tx data object
                        try:
                            tx = Tx(
                                timestamp=datetime.now(),
                                raw_data=str(data)
                            )

                            # add, commit and flush
                            db_session.add(tx)
                            db_session.commit()
                            db_session.flush()

                            # new ID from our tx
                            tx_id = tx.id

                            # set the decoded header to a list obj
                            items = list(decoded.items())

                            # access the list members
                            product_type = items[0][1]
                            hardware_rev = items[1][1]
                            firmware_rev = items[2][1]
                            contact_reason = items[3][1]
                            alarm_status = items[4][1]
                            imei = items[5][1]
                            gsm_rssi = items[6][1]
                            battery_status = items[7][1]
                            message_type = items[8][1]
                            payload_len = items[9][1]

                            # print a few vars from the list for debugging
                            print('Decoded Header: {}'.format(decoded))
                            print('Items from List: {}'.format(items))
                            print('Product Type: {}'.format(product_type))
                            print('Message Type: {}'.format(message_type))
                            print('IMEI: {}'.format(imei))
                            print('Payload Length: {}'.format(payload_len))

                            # write our message header and include the new tx_id
                            try:
                                tx_header = TxHeader(
                                    tx_id=tx_id,
                                    timestamp=datetime.now(),
                                    product_type=product_type,
                                    hardware_rev=hardware_rev,
                                    firmware_rev=firmware_rev,
                                    contact_reason=contact_reason,
                                    alarm_status=alarm_status,
                                    gsm_rssi=gsm_rssi,
                                    battery_status=battery_status,
                                    imei=imei,
                                    message_type=message_type,
                                    payload_len=payload_len
                                )

                                # add new tx_header obj, commit and flush
                                db_session.add(tx_header)
                                db_session.commit()
                                db_session.flush()

                                # assign new tx_header.id to variable for tx readings
                                tx_header_id = tx_header.id

                                # begin processing the readings
                                readings_data = data[52:]

                                # if the data contains a comma and Z=, strip it off
                                if ',Z=' in readings_data:
                                    clean_data = readings_data.split(',Z=')
                                    readings_data = clean_data[0]

                                # continue to process the tx data readings
                                # readings returns a list of 8 byte value to convert
                                for _ in range(payload_len - 1):
                                    readings = inspect_header(readings_data, 8)

                                # create our tx readings database records for the radio
                                for reading in readings:

                                    # decode the reading
                                    decoded_reading = decode_readings(reading)

                                    # insert to database
                                    tx_reading = TxReading(
                                        tx_id=tx_id,
                                        tx_header_id=tx_header_id,
                                        timestamp=decoded_reading.timestamp,
                                        distance=decoded_reading.distance,
                                        src=decoded_reading.src,
                                        rssi=decoded_reading.rssi,
                                        temperature=decoded_reading.temperature
                                    )

                                    # commit to the database
                                    db_session.add(tx_reading)
                                    db_session.commit()

                                # dump the readings values to the console
                                print('Tx Header ID: {}'.format(tx_header_id))
                                print('Tx Reading Data: {}'.format(readings_data))
                                continue

                            # inner database exception
                            except exc.SQLAlchemyError as err:
                                print('Database returned error: {}'.format(str(err)))

                        # outer database exception
                        except exc.SQLAlchemyError as err:
                            print('Database returned error: {}'.format(str(err)))

                    # incoming data stream could not be decoded
                    # close the connection
                    else:
                        print('The data in the buffer could not be decoded.  Aborting connection.')
                        print('Data: {}'.format(tx))
                        connection.close()

                # end of data from client
                else:
                    print('No more data from {}'.format(client_address))
                    break

        # socket error
        except socket.error as socket_err:
            print('Socket returned error: {}'.format(socket_err))
            sys.exit(1)


if __name__ == '__main__':
    """
    Start the Python Socket Server and Listen for Connections.
    Network Receiver Listens on Port 9060
    """
    # create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to the port
    server_address = '0.0.0.0'
    # should be socket.gethostname()
    port = 8060

    # bind the server address
    s.bind((server_address, port))

    # flash a server message to console
    print('Socket server starting up... listening on {}, Port: {}'.format(server_address, port))

    # listen for incoming connections
    s.listen(1)

    # call main program
    main()
