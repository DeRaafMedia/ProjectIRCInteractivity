__author__ = 'DeRaaf'
# TODO Clean up comments. Fix bugs. On going project!

import serial


class SerialPort(object):

    def __init__(self,
                 serial_port,
                 baud_rate,
                 time_out):

        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.time_out = time_out
        self.serializer = serial.Serial(port=self.serial_port,
                                        baudrate=self.baud_rate,
                                        timeout=self.time_out,
                                        writeTimeout=self.time_out)

    def __str__(self):
        return '\n\nSerial port : {0}\n' \
               'Baud Rate : {1}\n' \
               'Time Out : {2}' \
               '\n\n'.format(self.serial_port,
                             self.baud_rate,
                             self.time_out)

    def __getattr__(self):
        return 'Not found'.format()

    def connect_serial_port(self):
        return serial.Serial(port=self.serial_port,
                             baudrate=self.baud_rate,
                             timeout=self.time_out,
                             writeTimeout=self.time_out)

    def open_serial_port(self):
        """
        Opens the Serial port
        :return:
        """
        # Method to open the serial port. Not needed in normal use cases. push_data/pull_data do this automatic
        return 'open_serial_port'
        #self.serializer.open()

    def close_serial_port(self):
        """
        Closes the Serial port
        :return:
        """
        # Method to close the serial port. Not needed in normal use cases. push_data/pull_data do this automatic
        return 'close_serial_port'
        #self.serializer.close()

    def push_data(self,
                  serial_tx):
        """
        serial_tx -> The data you want to send to the Arduino as a quoted string (i.e 'Test message')
        Most of the time msg is used from other functions
        :param serial_tx:
        :return:
        """
        # Write serial data to receiver (Arduino)
        #return 'push_data'
        self.serializer.write(serial_tx)

    def pull_data(self):
        """
        Pulls data from the Arduino.
        :return:
        """
        # Read serial data to receiver (Arduino)
        return 'pull_data'
        #return self.serializer.readline()

    def serial_flush(self):
        """
        Flush serial buffers after file transfer
        :return:
        """
        return 'serial_flush'
        #self.serializer.flush()

    def serial_flush_in(self):
        """
        Flush the incoming (rx) serial port
        :return:
        """
        return 'serial_flush_in'
        #self.serializer.flushInput()

    def serial_flush_out(self):
        """
        Flush the outgoing (tx) serial port
        :return:
        """
        return 'serial_flush_out'
        #self.serializer.flushOutput()