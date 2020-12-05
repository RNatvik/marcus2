import json
import serial
import struct
import time


def create_read_msg(regs: list, register_map: dict):
    header = struct.pack('B', 0xff) + struct.pack('B', 0xaa) + struct.pack('B', len(regs))
    msg = b''
    for r in regs:
        msg += struct.pack('B', register_map[r]['num'])
    return header + msg


def create_write_msg(regs: list, register_map: dict):
    header = struct.pack('B', 0xff) + struct.pack('B', 0xbb) + struct.pack('B', len(regs))
    msg = b''
    for r, v in regs:
        msg += struct.pack('B', register_map[r]['num'])
        msg += struct.pack(register_map[r]['type'][0], v)
    return header + msg


def read(regs: list, ser: serial.Serial, register_map: dict):
    data = {}
    expected_bytes = sum([register_map[r]['type'][1] for r in regs])
    response = ser.read(expected_bytes)
    i0 = 0
    for r in regs:
        i = i0 + register_map[r]['type'][1]
        part = response[i0:i]
        data[r] = struct.unpack(register_map[r]['type'][0], part)[0]
        i0 = i
    return data


def main():
    port = "COM5"
    baudrate = 115200
    timeout = 2

    with open('registers.json', 'r') as f:
        registers = json.load(f)

    with serial.Serial(port=port, baudrate=baudrate, timeout=timeout) as ser:
        time.sleep(3)

        wregs = ['loop_time', 'pitch']
        wvalues = [1000, 10]

        msg = create_write_msg(list(zip(wregs, wvalues)), registers)
        ser.write(msg)
        initial_response = ser.read(1)
        print(initial_response)

        regs = ['pitch', 'roll', 'yaw', 'loop_time', 'rax', 'ray', 'raz', 'rgx', 'rgy', 'rgz', 'rmx', 'rmy', 'rmz']

        msg = create_read_msg(regs, registers)
        ser.write(msg)
        initial_response = ser.read(1)
        print(initial_response)
        data = read(regs, ser, registers)
        print(data)


if __name__ == '__main__':
    main()
