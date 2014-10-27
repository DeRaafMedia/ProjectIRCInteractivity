import sys
import serial


def function_name(arg_1, arg_2, arg_3, arg_4):

    serial_port = str(arg_1)
    baud_rate = int(arg_2)
    time_out = int(arg_3)
    parameter = int(arg_4)

    # Function here

    pass

if __name__ == "__function_name__":
    function_name(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    pass
