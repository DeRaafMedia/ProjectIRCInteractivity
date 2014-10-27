__author__ = 'DeRaaf'
# TODO Clean up comments. Fix bugs. On going project!

from SerialPort import *

class Arduino(SerialPort):

    def __init__(self,
                 serial_port_id):
        """
        serial_port_id -> Give the serial port id as a variable name (i.e serial_port_2)
        Object can be addressed but serves as glue between SerialPort and Pin
        :param serial_port_id:
        :return:
        """
        super(Arduino, self).__init__(serial_port_id.serial_port,
                                      serial_port_id.baud_rate,
                                      serial_port_id.time_out)
        self.arduino_attr = SerialPort(self.serial_port,
                                       self.baud_rate,
                                       self.time_out)

    def __str__(self):
        return '\n\nSerial port: {0}\n' \
               'Baudrate : {1}\n' \
               'Time Out : {2}' \
               '\n\n'.format(self.serial_port,
                             self.baud_rate,
                             self.time_out)

    def __getattr__(self):
        return 'Not Found'.format()

    def soft_reset(self):
        """
        Function to perform a soft reset of the Arduino
        """
        self.push_data('{0}/{1}/'.format(3, 3))


class Pin(Arduino):

    def __init__(self,
                 arduino_id,
                 pin_number,
                 pin_type):
        """
        arduino_id -> Give the arduino id as a variable name (i.e arduino_1)
        pin_number -> Give the number of a pin as an int (i.e 10)
        pin_type -> Give he type of pin four possible (i.e 'analog_in', 'analog_out', 'digital_in' and 'digital_out')
        Pin object. This function makes individual pins on Arduino addressable
        :param arduino_id:
        :param pin_number:
        :param pin_type:
        :return:
        """
        super(Pin, self).__init__(arduino_id)
        self.pin_number = pin_number
        self.pin_type = pin_type
        self.close_serial_port()

    def __str__(self):
        return '\n\nPin number: {0}\n' \
               'Pin type: {1}' \
               '\n\n'.format(self.pin_number,
                             self.pin_type)

    def analog_read(self):
        """
        Analog read function not yet implemented
        :return:
        """
        if self.pin_type != 'analog_in':
            print('\nError: Pin needs to be analog_in. Pin {0} on {1} is {2}'
                  '\n'.format(self.pin_number,
                              self.serial_port,
                              self.pin_type))
        else:
            # TODO read analog function.
            print('\nGood to go\n')

    def analog_write(self,
                     analog_value):
        """
        analog_value -> A value between 0 - 255 (i.e 125)
        Function handles the analog write communications for specified pin
        :param analog_value:
        :return:
        """
        if self.pin_type != 'analog_out':
            print('\nError: Pin needs to be analog_out. Pin {0} on {1} is {2}'
                  '\n'.format(self.pin_number,
                              self.serial_port,
                              self.pin_type))
        else:
            self.push_data('{0}/{1}/{2}/{3}/'.format(1,
                                                     1,
                                                     self.pin_number,
                                                     analog_value))

    def digital_read(self):
        """
        Digital read function not yet implemented
        :return:
        """
        if self.pin_type != 'digital_in':
            print('\nError: Pin needs to be digital_in. Pin {0} on {1} is {2}'
                  '\n'.format(self.pin_number,
                              self.serial_port,
                              self.pin_type))
        else:
            print('\nGood to go\n')

    def digital_write(self,
                      digital_value):
        """
        digital_value -> Binary 0 is LOW (false) or 1 is HIGH (true)
        :param digital_value:
        :return:
        """
        if self.pin_type != 'digital_out':
            print('\nError: Pin needs to be digital_out. Pin {0} on {1} is {2}'
                  '\n'.format(self.pin_number,
                              self.serial_port,
                              self.pin_type))
        else:
            self.push_data('{0}/{1}/{2}/{3}/'.format(1,
                                                    2,
                                                    self.pin_number,
                                                    digital_value))