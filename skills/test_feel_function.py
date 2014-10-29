import sys
import serial
from time import sleep

def test_feel(arg_1, arg_2, arg_3, arg_4):

    serial_port = str(arg_1)
    baud_rate = int(arg_2)
    time_out = int(arg_3)
    parameter = int(arg_4)
    device = serial.Serial(serial_port, baud_rate, timeout=time_out)

    for i in range(0, 10000):

        device.write('1/1/11/0/')

        device.write('1/2/22/1/')
        device.write('1/2/24/2/')

        device.write('2/2/23/')

        x = int(device.readline().strip())

        print(x)

        if x == 1:
            device.write('1/2/9/2/')
        else:
            device.write('1/2/9/1/')

    device.write('1/1/9/0/')
    device.write('1/2/22/1/')
    device.write('1/1/24/1/')
    device.close()

if __name__ == "__test_feel__":
    test_feel(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])