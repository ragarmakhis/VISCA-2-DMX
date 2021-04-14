acknowledge_message = bytearray.fromhex('90 4Y FF'.replace('Y', '1'))  # 1 = socket number
completion_message = bytearray.fromhex('90 5Y FF'.replace('Y', '1'))

visca_command_dictionary = {
    b'81010601': 'pan/tilt',
    b'81010602': 'absolute_position',
    b'81010603': 'relative_position',
    b'81010604': 'home',
    b'81010408': 'focus',
    b'81010438': 'autofocus',
    b'81010407': 'zoom',
    b'8101043f': 'memory',
    b'81017e01': 'information_display',
    b'81010400': 'camera_power',
    b'01': 'reset_sequence_number'
    }
direction_dictionary = {
    b'0301': 'Up',
    b'0302': 'Down',
    b'0103': 'Left',
    b'0203': 'Right',
    b'0101': 'UpLeft',
    b'0201': 'UpRight',
    b'0102': 'DownLeft',
    b'0202': 'DownRight',
    b'0303': 'Stop'
}
pan_tilt_speed_dictionary = {
    b'01': 1.1,
    b'02': 1.3,
    b'03': 1.4,
    b'04': 2.2,
    b'05': 2.9,
    b'06': 6.7,
    b'07': 11,
    b'08': 23,
    b'09': 24,
    b'0a': 27,
    b'0b': 41,
    b'0c': 43,
    b'0d': 47,
    b'0e': 49,
    b'0f': 54,
    b'10': 57,
    b'11': 62,
    b'12': 64,
    b'13': 69,
    b'14': 72,
    b'15': 80,
    b'16': 84,
    b'17': 91,
    b'18': 101
}