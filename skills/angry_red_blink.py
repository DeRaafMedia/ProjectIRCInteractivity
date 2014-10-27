import sys
import serial
from time import sleep

def angry_red_blink(arg_1, arg_2, arg_3, arg_4):

    serial_port = str(arg_1)
    baud_rate = int(arg_2)
    time_out = int(arg_3)
    parameter = int(arg_4)

    device = serial.Serial(serial_port, baud_rate, timeout=time_out)

    x = 0
    for i in range(0, parameter):
        while x < 255:
            device.write('1/1/11/' + str(x) + '/')
            sleep(0.00001)
            x += 1
            sleep(0.00001)
        sleep(0.00001)
        while x > 0:
            device.write('1/1/11/' + str(x) + '/')
            sleep(0.00001)
            x -= 1
            sleep(0.00001)
        sleep(0.00001)

    device.write('1/1/11/0/')
    device.close()


if __name__ == "angry_red_blink":
    angry_red_blink(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
