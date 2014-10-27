import sys
import serial
from time import sleep


def hello_world(arg_1, arg_2, arg_3, arg_4):
    serial_port = str(arg_1)
    baud_rate = int(arg_2)
    time_out = int(arg_3)
    parameter = int(arg_4)

    device = serial.Serial(serial_port, baud_rate, timeout=time_out)

    y = 255
    x = 0
    for i in range(0, parameter):
        while x < 255:
            device.write('1/1/13/' + str(x) + '/')
            sleep(0.003)
            device.write('1/1/12/' + str(y) + '/')
            sleep(0.003)
            if y > 128:
                device.write('1/1/11/0/')
            x = x + 1
            y = y - 1
            # print(x)
            # print(y)
            sleep(0.003)
        sleep(0.003)
        while x > 0:
            device.write('1/1/13/' + str(x) + '/')
            sleep(0.003)
            device.write('1/1/12/' + str(y) + '/')
            sleep(0.003)
            if y < 128:
                device.write('1/1/11/3/')
            x = x - 1
            y = y + 1
            # print(x)
            # print(y)
            sleep(0.003)
        sleep(0.003)

    device.write('1/1/11/0/')
    device.write('1/1/12/0/')
    device.write('1/1/13/0/')
    device.close()

if __name__ == "__hello_world__":
    hello_world(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])