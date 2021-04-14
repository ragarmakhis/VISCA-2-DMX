from sys import exit as sys_exit
import socket
from time import sleep
import binascii

# import keyboard

from visca import visca_command_dictionary, direction_dictionary, pan_tilt_speed_dictionary
from visca import acknowledge_message, completion_message

port = 52381
buffer_size = 1024

_current_position = {'pan': 0, 'tilt': 0}


def get_current_position():
    return _current_position


def set_current_position(pan, tilt):
    _current_position['pan'] = pan
    _current_position['tilt'] = tilt


def get_speeds(message_data):
    pan_speed = message_data[0:2]
    tilt_speed = message_data[2:4]
    return pan_speed, tilt_speed


def get_coordinates(message_data):
    pan_pos = message_data[4:12].replace(b'0', b'')
    # pan_in_bytes = int(f'0x{pan_pos.decode()}', base=16).to_bytes(2, byteorder='big')
    pan_in_bytes = int(pan_pos, 16).to_bytes(2, byteorder='big')
    pan_coordinate = int.from_bytes(pan_in_bytes, byteorder='big', signed=True)
    tilt_pos = message_data[12:20].replace(b'0', b'')
    # tilt_in_bytes = int(f'0x{tilt_pos.decode()}', base=16).to_bytes(2, byteorder='big')
    tilt_in_bytes = int(tilt_pos, 16).to_bytes(2, byteorder='big')
    tilt_coordinate = int.from_bytes(tilt_in_bytes, byteorder='big', signed=True)
    return pan_coordinate, tilt_coordinate


def move_camera(direction, pan_speed, tilt_speed):
    pan_delta = 1
    tilt_delta = 1
    print(f'direction = {direction} with pan speed = {pan_speed} degrees and tilt '
          f'speed = {tilt_speed} degrees')
    pan_pos = get_current_position()['pan']
    tilt_pos = get_current_position()['tilt']
    if direction == 'UpLeft':
        pan_pos += pan_delta
        tilt_pos += tilt_delta
    elif direction == 'Up':
        tilt_pos += tilt_delta
    elif direction == 'UpRight':
        pan_pos -= pan_delta
        tilt_pos += tilt_delta
    elif direction == 'Left':
        pan_pos += pan_delta
    elif direction == 'Right':
        pan_pos -= pan_delta
    elif direction == 'DownLeft':
        pan_pos += pan_delta
        tilt_pos -= tilt_delta
    elif direction == 'Down':
        tilt_pos -= tilt_delta
    elif direction == 'DownRight':
        pan_pos -= pan_delta
        tilt_pos -= tilt_delta
    print(f'camera rotate in pan = {pan_pos} and tilt = {tilt_pos}')
    set_current_position(pan_pos, tilt_pos)


def set_camera_position(pan_coordinate, tilt_coordinate, pan_speed, tilt_speed, absolute_position=False):
    if not absolute_position:
        pan_coordinate += get_current_position()['pan']
        tilt_coordinate += get_current_position()['tilt']
    print(f'setting camera position with pan value = {pan_coordinate} and tilt value = {tilt_coordinate}')
    print(f'pan speed = {pan_speed}, tilt speed = {tilt_speed}')
    set_current_position(pan_coordinate, tilt_coordinate)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))

    # while keyboard.is_pressed('F3'):
    while True:
        message, address_port = s.recvfrom(buffer_size)
        # payload_type = message[0:2]
        # payload_length = int(binascii.hexlify(message[2:4]), 16)
        sequence_number = int(binascii.hexlify(message[4:8]), 16)
        payload = binascii.hexlify(message[8:])
        # print(message[8:])
        message_type = payload[0:8]
        message_data = payload[8:]
        try:
            print(f'{sequence_number} {visca_command_dictionary[message_type]} message = {message_data}')
            if visca_command_dictionary[message_type] == 'pan/tilt':
                pan_speed, tilt_speed = get_speeds(message_data)
                direction = direction_dictionary[message_data[4:8]]
                move_camera(direction, pan_tilt_speed_dictionary[pan_speed], pan_tilt_speed_dictionary[tilt_speed])
            if visca_command_dictionary[message_type] == 'absolute_position'\
                    or visca_command_dictionary[message_type] == 'relative_position':
                pan_speed, tilt_speed = get_speeds(message_data)
                pan_coordinate, tilt_coordinate = get_coordinates(message_data)
                absolute_position = True if visca_command_dictionary[message_type] == 'absolute_position' else False
                set_camera_position(pan_coordinate, tilt_coordinate, pan_speed, tilt_speed,
                                    absolute_position=absolute_position)
        except KeyError:
            print(sequence_number, payload, message_type)
        s.sendto(acknowledge_message, address_port)
        sleep(0.1)
        s.sendto(completion_message, address_port)

        # if keyboard.is_pressed('F3'):
        if None:
            return 0

    # return 0


if __name__ == "__main__":
    sys_exit(main())
