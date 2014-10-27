import serial
from time import sleep
import random
import sys


def erratic_blink(arg_1, arg_2, arg_3, arg_4):
    serial_port = str(arg_1)
    baud_rate = int(arg_2)
    time_out = int(arg_3)
    parameter = int(arg_4)

    print(serial_port)
    print(baud_rate)
    print(time_out)
    print(parameter)
    print('-------------------------------------------------------')

    device = serial.Serial(serial_port, baud_rate, timeout=time_out)

    for i in range(0, parameter):
        device.write('1/1/13/' + str(random.randrange(0, 250, 25)) + '/')
        sleep(random.uniform(0.01, 0.07))
        device.write('1/1/12/' + str(random.randrange(0, 250, 25)) + '/')
        sleep(random.uniform(0.01, 0.07))
        device.write('1/1/11/' + str(random.randrange(0, 250, 25)) + '/')
        sleep(random.uniform(0.01, 0.07))

    device.write('1/1/11/0/')
    device.write('1/1/12/0/')
    device.write('1/1/13/0/')
    device.close()

if __name__ == "__erratic_blink__":
    erratic_blink(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])