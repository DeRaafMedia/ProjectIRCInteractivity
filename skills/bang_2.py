import sys
import serial


def bang_1(arg_1, arg_2, arg_3, arg_4):

    serial_port = str(arg_1)
    baud_rate = int(arg_2)
    time_out = int(arg_3)
    parameter = int(arg_4)

    device = serial.Serial(serial_port, baud_rate, timeout=time_out)
    device.write('1/1/9/' + parameter + '/')

if __name__ == "__bang_1__":
    bang_1(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])