# .env/bin/python
# coding: utf-8

from collections import namedtuple
from datetime import datetime


def pad_reading(_reading):
    """
    Return a full binary representation of the individual bytes
    :param _reading:
    :return: binary
    """
    prefix = 0

    for i in range(len(_reading) - 1):
        prefix += '0'

    return prefix


def hex_to_dec(hex_str):
    return int(str(hex_str), 16)


def bin_to_dec(binary_str):
    return sum([int(binary_str[-i]) * 2 ** (i - 1) for i in range(1, len(binary_str) + 1)])


def inspect_header(h, n):
    return [h[i:i+n] for i in range(0, len(h), n)]


def decode_header(header):
    """
    Decode the payload header and return a named tuple as an OrderedDict
    :param header: bytes representation of the first 32 bytes of data
    :return: OrderedDict
    """

    # define named tuple
    DecodedHeader = namedtuple('DecodedHeader', 'product_type, hardware_rev, firmware_rev, contact_reason, '
                                                'alarm_status, imei gsm_rssi, battery_status, message_type, '
                                                'payload_len')

    # start conversions: each byte has a different conversion method, so try this...
    # optionally, use data.decode('utf-8') in hex_to_dec function
    for idx, data in enumerate(header):
        # print(idx, data)
        if idx == 0:
            product_type = int(str(data), 16)
        elif idx == 1:
            hardware_rev = int(data, 2)
        elif idx == 2:
            firmware = bin(int(data, 16)).replace('0b', '')
            firmware_rev_minor = bin_to_dec(firmware[0:3])
            firmware_rev_major = bin_to_dec(firmware[4:8])
            firmware_rev = str(firmware_rev_major) + '.' + str(firmware_rev_minor)
        elif idx == 3:
            contact_reason = bin(int(data, 16))
        elif idx == 4:
            alarm_status = bin(int(data, 16))
        elif idx == 5:
            gsm_rssi = int(str(data), 16)
        elif idx == 6:
            battery_status = int(str(data), 16)
        elif idx == 15:
            message_type = int(str(data), 16)
        elif idx == 16:
            payload_len = int(str(data), 16)

    # create imei from the middle of the string
    imei_list = header[7:15]

    # the list elements are bytes, re-encode to create string
    imei = ''.join(str(i) for i in imei_list)

    # print vars
    print('Product Type: {}'.format(product_type))
    print('Hardware Rev: {}'.format(hardware_rev))
    print('Firmware Rev: {}'.format(firmware_rev))
    print('Contact Reason: {}'.format(contact_reason))
    print('Alarm Status: {}'.format(alarm_status))
    print('RSSI: {}'.format(gsm_rssi))
    print('Battery Status: {}'.format(battery_status))
    print('IMEI: {}'.format(imei))
    print('Message Type: {}'.format(message_type))
    print('Payload Length: {}'.format(payload_len))


    # set the variable to the decoded values
    hdr = DecodedHeader(product_type=product_type, hardware_rev=hardware_rev, firmware_rev=firmware_rev,
                        contact_reason=contact_reason, alarm_status=alarm_status, gsm_rssi=gsm_rssi,
                        battery_status=battery_status, imei=imei, message_type=message_type, payload_len=payload_len)

    # return hdr as an ordered dict
    return hdr._asdict()


def decode_readings(reading):
    """
    Decode the transmission readings from the payload
    :param hex reading:
    :return: decoded values
    """

    _reading = bin(int(reading, 16)).replace('0b', '')

    if len(_reading) < 32:
        _reading = pad_reading(_reading)

    distance, temperature, src, rssi = 0
    timestamp = datetime.now()

    # sample reading = 0A5B2877
    byte1 = _reading[0:8]    # 00001010
    byte2 = _reading[8:16]   # 01011011
    byte3 = _reading[16:24]  # 00101000
    byte4 = _reading[24:33]  # 01110111

    # concatenate upper and lower bits from 3 and 4
    # modify value for binary to hex to decode
    _distance = byte3[:2] + byte4
    _temp = hex(int(byte2, 2))
    _rssi = hex(int(byte1, 2))
    _src = byte3[2:6]

    decoded_reading = {
        'distance': bin_to_dec(_distance),
        'temperature': float(hex_to_dec(_temp)) / 2 * 30,
        'src': bin_to_dec(_src),
        'rssi': float(hex_to_dec(_rssi))
    }

    return decoded_reading
