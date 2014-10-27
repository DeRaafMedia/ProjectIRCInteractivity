__author__ = 'DeRaaf'

"""
EXAMPLE
"""

"""
These are the minimum on classes you need to import. If you want to hook up other devices than an Arduino take the
Arduino class (Ardiuno.py) as template to create a physical device with which this software can speak
"""

import sys
from SerialPort import *
from Arduino import *
from IRCBot import *


def main(arg_1,  # serial_port
         arg_2,  # baud_rate
         arg_3,  # time_out
         arg_4,  # serial_port_id
         arg_5,  # physical_device_id
         arg_6,  # bot_name
         arg_7,  # bot_owner
         arg_8,  # irc_network
         arg_9,  # irc_port
         arg_10):  # irc_channel
    """
    :param arg_1:
    :param arg_2:
    :param arg_3:
    :param arg_4:
    :param arg_5:
    :param arg_6:
    :param arg_7:
    :param arg_8:
    :param arg_9:
    :param arg_10:
    :return:
    """
    serial_port = arg_1  # Write your own setting instead of arg_1
    baud_rate = arg_2  # Write your own setting instead of arg_2
    time_out = arg_3  # Write your own setting instead of arg_3
    serial_port_id = arg_4  # Write your own setting instead of arg_4
    physical_device_id = arg_5  # Write your own setting instead of arg_5
    bot_name = arg_6  # Write your own setting instead of arg_6
    bot_owner = arg_7  # Write your own setting instead of arg_7
    irc_network = arg_8  # Write your own setting instead of arg_8
    irc_port = arg_9  # Write your own setting instead of arg_9
    irc_channel = arg_10  # Write your own setting instead of arg_10

    """
    This code can be replaced with:

    serial_port_id = SerialPort('/dev/your_serial_port',
                                115200,
                                2,
                                'serial_port_id')
    """
    initiate_serial_port = (serial_port_id
                            + ' = SerialPort("'
                            + serial_port
                            + '", '
                            + baud_rate
                            + ', '
                            + time_out
                            + ', "'
                            + serial_port_id
                            + '")')

    exec initiate_serial_port

    """
    This code can be replaced with:

    physical_device_id = PhysicalDevice(serial_port_id,
                                        physical_device_id)
    """
    initiate_physical_device = (physical_device_id
                                + ' = Arduino('
                                + serial_port_id
                                + ', "'
                                + physical_device_id
                                + '")')

    exec initiate_physical_device

    """
    This code can be replaced with:

    robby_the_robot = IRCBot('irc.freenode.net',  # The IRC channel you want to use
                             6667,  # The IRC channels port number
                             '#YourChatChannel',  # The IRC channel name
                             'RobbyTheRobot',  # The name of the IRCBot (Same name as folder of Brain.csv)
                             'TheBotOwner',
                             physical_device_id,
                             serial_port_id)
    """
    initiate_ircbot = (bot_name
                       + ' = IRCBot("'
                       + irc_network
                       + '", '
                       + irc_port
                       + ', "'
                       + irc_channel
                       + '", "'
                       + bot_name
                       + '", "'
                       + bot_owner
                       + '", '
                       + physical_device_id
                       + ', '
                       + serial_port_id
                       + ')')

    exec initiate_ircbot

    start_ircbot = (bot_name + '.listen("no", "no")')

    exec start_ircbot

if __name__ == '__main__':
    """
    This code makes this function executable from terminal with the following arguments:

    Serial port : '/dev/your_port'
    Baud Rate : '115200'
    Time Out : '2' (Sometimes needed to troubleshoot)
    A name for the Serial Port : 'serial_port_1'
    A name for the Physical Device you want to use : 'arduino_1'
    A name for the IRCBot : 'Robby_The_Robot' (needs to be the same name as the folder with the Brain.csv file!!)
    The owner of the IRCBot : YourChatNickName
    The IRC network : 'irc.freenode.net'
    The IRC port : 6667
    The IRC channel : '#YourChannel'

    Terminal command: (one line)

    $ python startIRCInteractivity.py
             'your/serial_device'
             '115200'
             '2'
             'serial_port_1'
             'arduino_1'
             'RobbyTheRobot'
             'DeRaaf'
             'irc.freenode.net'
             '6667'
             '##SandBoxDeRaaf'
    """
    main(sys.argv[1],
         sys.argv[2],
         sys.argv[3],
         sys.argv[4],
         sys.argv[5],
         sys.argv[6],
         sys.argv[7],
         sys.argv[8],
         sys.argv[9],
         sys.argv[10])