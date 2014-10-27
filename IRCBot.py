__author__ = 'DeRaaf'
# TODO Clean up comments. Fix bugs. On going project!

import socket
from time import sleep
import time

from Utilities import *


def load_imports(path_to_skills):
    """
    path_to_skills -> Path to the skills directory (i.e 'skills/')

    This function takes in al of the skill script files and puts them into the __init__.py file so the directory
    (and all skills in it) can be imported for use.

    :param path_to_skills:
    """
    files = os.listdir(path_to_skills)
    skill_scripts = []

    for i in range(len(files)):
        name = files[i].split('.')
        if len(name) > 1:
            if name[1] == 'py' and name[0] != '__init__':
                name = name[0]
                skill_scripts.append(name)

    init_file = open(path_to_skills+'__init__.py', 'w')

    to_write = '__all__ = '+str(skill_scripts)

    init_file.write(to_write)
    init_file.close()

load_imports('skills/')

from skills import *


class IRCBot(object):

    def __init__(self,
                 irc_network,
                 irc_port,
                 irc_channel,
                 irc_bot_nick,
                 irc_bot_owner,
                 physical_device_id,
                 serial_port_id):
        """
        irc_network -> Give address of IRC chat as quoted string (i.e 'irc.freenode.net')
        irc_channel -> Give the name of the IRC channel as quoted string (i.e '#FooChannel')
        irc_port -> Give the port number which IRC is using (i.e 6667)
        irc_bot_nick -> Give a name to the IRC bot. This name needs to be same as you used for it's 'Brain'. But replace
                        underscores (_) with spaces if you use them. i.e the Brain.cvs is called Robby_The_Robot.cvs
                        the robot name has to be 'Robby the Robot'. Upper/lower cases are important!
        irc_bot_owner -> The name that you use as a IRC handle. Feature is handy when you want to invent something where
                         two bots battle in the name of it's owners or something

        # TODO buy some other physical devices (MSP or something) to see how this code can be made more universal
        physical_device -> Give a name to the physical device you connected (i.e arduino_1)
        pins -> Give the list of pins you are gonna use on this device (fairly specific for the Arduino object)
        serial_port -> The serial port you device is connected to (i.e /dev/tty.usb-yourdevice)
        baud_rate -> The Baud rate the device is using
        time_out -> Needed to handle time outs on the serial port. I wrote this software with a time out of 2. Never had
                    a problem.

        speak_enabled -> Very specific for Mac use. If the speak is enables than you can make functions and reactions
                          where the computer used is talking with a physical voice.

        spy -> Enable or Disable IRC chat log. The log files are stored in the logs/chat directory. Every chat session
               gets it own file.

        Set the IRC variables and create the IRC socket object

        Set the physical device variables

        :param irc_network:
        :param irc_channel:
        :param irc_bot_nick:
        :param irc_bot_owner:
        :param physical_device_id:
        :param serial_port_id:
        """
        self.think_tasks_array = []
        self.speak_tasks_array = []
        self.chat_speak_array = []
        self.act_tasks_array = []
        self.feel_tasks_array = []
        self.combined_tasks_array = []

        self.irc_network = irc_network
        self.irc_port = irc_port
        self.irc_channel = irc_channel
        self.irc_bot_nick = irc_bot_nick
        self.irc_bot_owner = irc_bot_owner
        self.irc_bot_voice = ''

        self.physical_device = physical_device_id
        self.serial_port = serial_port_id.serial_port
        self.baud_rate = serial_port_id.baud_rate
        self.time_out = serial_port_id.time_out
        self.spy = ''

        self.chat_directory = 'logs/chat/'
        self.timestamp = time.strftime('%m%d%Y%H%M')
        self.chat_log_file_name = ''  # Initial value for the chat log file name
        self.irc_socket = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)  # Initiate socket

        self.speak_enabled = ''  # Initial value of speak enabled
        self.chat_speak_enabled = ''
        self.start_thinking = False

        self.preference_file = 'pref/preferences.txt'
        self.preferences = Utilities()

        self.thread = Utilities()
        self.speech = Utilities()
        self.incoming_conversation = Utilities()

    def __str__(self):
        return '\n\nIRC Network: {0}\n' \
               'IRC Port: {1}\n' \
               'IRC Channel: {2}\n' \
               'IRC NickName: {3}\n' \
               'IRC Bot Owner: {4}\n' \
               'IRC Bot Voice : {5}' \
               'Physical Device: {6}\n' \
               'Serial Port: {8}\n' \
               'Baud Rate: {9}\n' \
               'Time Out: {10}\n' \
               '\n\n'.format(self.irc_network,
                             self.irc_port,
                             self.irc_channel,
                             self.irc_bot_nick,
                             self.irc_bot_owner,
                             self.irc_bot_voice,
                             self.physical_device,
                             self.serial_port,
                             self.baud_rate,
                             self.time_out)

    def __getattr__(self):
        return '{0}'.format('Not Found')

    def load_preferences(self):
        self.preferences.initiate(self.preference_file)

    def handle_preferences(self):
        self.spy = self.preferences.read(self.preference_file,
                                         'Log Settings',
                                         'chat')
        self.speak_enabled = self.preferences.read(self.preference_file,
                                                   'Speak',
                                                   'speak_enabled')
        self.chat_speak_enabled = self.preferences.read(self.preference_file,
                                                        'Speak',
                                                        'chat_speak_enabled')
        self.irc_bot_voice = self.preferences.read(self.preference_file,
                                                   'Voices',
                                                   'default')

    def irc_connect(self):
        """
        Connect to give IRC channel

        :rtype : object
        """
        self.irc_socket.connect((self.irc_network,
                                 self.irc_port))
        if self.spy == 'yes':
            if not os.path.exists(self.chat_directory):
                os.makedirs(self.chat_directory, mode=0755)
            self.chat_log_file_name = self.timestamp+'.txt'
            log_file = open((self.chat_directory + self.chat_log_file_name), "a")
            log_file.write(self.irc_socket.recv(4096).strip()+'\n')
        else:
            pass

    def get_born(self):
        """
        Connects IRCBot to IRC and let's make itself know

        """
        self.irc_connect()
        self.irc_socket.send('NICK ' + self.irc_bot_nick + '\r\n')
        self.irc_socket.send('USER ' + self.irc_bot_nick + ' 0 * :' + self.irc_bot_owner + '\r\n')
        self.irc_socket.send('JOIN ' + self.irc_channel + '\r\n')
        self.irc_socket.send('PRIVMSG ' + self.irc_channel + ' :Hello World. My name is ' + self.irc_bot_nick + '\r\n')

    def survive(self,
                conversation):
        """
        conversation -> Passed from listen function

        PING response function. Because every PING deserves a appropriate PONG response

        :param conversation:
        :rtype : object
        """
        self.irc_socket.send('PONG ' + conversation.split()[1] + '\r\n')
        print('PONG')  # TEST PRINT

    def listen(self,
               as_thread,
               as_daemon):
        """
        as_thread -> 'yes' if this method needs to be executed as a thread, 'no' if it doesn't
        as_daemon -> 'yes' if this method needs to be executed as a daemon, 'no' if it doesn't

        To thread or not to thread was the question. I wrote in threading functionality for future use (maybe starting
        today???). Default behaviour is to start functions as procedural (inline with main script) processes.

        :param as_thread:
        :param as_daemon:
        :rtype : object
        """
        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.thread.new_thread('yes',
                                       self.listen_function,
                                       'none')
            else:
                self.thread.new_thread('no',
                                       self.listen_function,
                                       'none')
        else:
            self.listen_function()

    def listen_function(self):
        """
        Puts the individual IRC conversation in a task list so the think function can handle it one 'thought' at a time.

        :return:
        """
        self.load_preferences()
        self.handle_preferences()
        self.get_born()
        while True:
            conversation = self.irc_socket.recv(4096)
            if conversation.find('PING') != -1:
                self.survive(conversation)
            else:
                if conversation:
                    sleep(0.2)
                    self.think('no', 'no', conversation)

    def think(self,
              as_thread,
              as_daemon,
              conversation):
        """
        as_thread -> 'yes' if this method needs to be executed as a thread, 'no' if it doesn't
        as_daemon -> 'yes' if this method needs to be executed as a daemon, 'no' if it doesn't

        To thread or not to thread was the question. I wrote in threading functionality for future use (maybe starting
        today???). Default behaviour is to start functions as procedural (inline with main script) processes.

        :param as_thread:
        :param as_daemon:
        :return:
        """
        self.think_tasks_array.append(conversation)

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.thread.new_thread('yes',
                                       self.think_function,
                                       'none')
            else:
                self.thread.new_thread('no',
                                       self.think_function,
                                       'none')
        else:
            self.think_function()

    def think_function(self):
        """
        Takes the think tasks list from the listen function and checks them against
        a CSV file with keywords and their appropriate response.
        Brain.csv is to be placed in the
        'appFolder -> brains -> <irc_bot_nick> (With underscores for spaces i.e Robby_The_Robot) -> Brain.csv'

        :return:
        """
        for task in self.think_tasks_array:

            if task.find('toggleChatLog') != -1:
                if self.spy == 'yes':
                    self.spy = 'no'
                    self.preferences.write(self.preference_file,
                                           'Log Settings',
                                           'chat',
                                           'no')
                else:
                    self.spy = 'yes'
                    self.preferences.write(self.preference_file,
                                           'Log Settings',
                                           'chat',
                                           'yes')

            if self.spy == 'yes':
                log_file = open((self.chat_directory + self.chat_log_file_name), "a")  # chat log file
                log_file.write(task)

            if task.find('End of /NAMES list') != -1:
                if not self.start_thinking:
                    self.start_thinking = True

            if self.start_thinking:

                self.chat_speak('no', 'no', task)

                execute = self.incoming_conversation.check_conversation(task, self.irc_bot_nick)

                if execute:

                    if execute[1] == 'yes':
                        pass

                    self.speak('yes', 'no', execute[2], execute[3])



                    if execute[7] != 'no':
                        self.act('yes',
                                 'no',
                                 execute[7],
                                 self.serial_port,
                                 self.baud_rate,
                                 self.time_out,
                                 execute[8])

                    # print('{0}').format(execute[9])

            del self.think_tasks_array[0]

    def speak(self,
              as_thread,
              as_daemon,
              conversation,
              voice):
        """
        as_thread -> 'yes' if this method needs to be executed as a thread, 'no' if it doesn't
        as_daemon -> 'yes' if this method needs to be executed as a daemon, 'no' if it doesn't
        voice -> A voice name used on Mac OSX system as a quoted string. Gets passed from Brain.csv (i.e 'Alex')

        Takes a string from the think function and sends it to IRC

        :param as_thread:
        :param as_daemon:
        :param voice:
        :return:
        """
        self.speak_tasks_array.append(conversation)

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.thread.new_thread('yes',
                                       self.speak_function,
                                       voice)
            else:
                self.thread.new_thread('no',
                                       self.speak_function,
                                       voice)
        else:
            self.speak_function(voice)

    def speak_function(self,
                       voice):
        """
        voice -> A voice name used on Mac OSX system as a quoted string. Gets passed from Brain.csv (i.e 'Alex')

        Executes the chat speak (the communication coming from others) if enabled as an parallel (threaded)
        object to main script

        :param voice:
        :return:
        """
        for task in self.speak_tasks_array:

            if task.find('toggleSpeak') != -1:
                if self.speak_enabled == 'yes':
                    self.speak_enabled = 'no'
                    self.preferences.write(self.preference_file,
                                           'Speak',
                                           'speak_enabled',
                                           'no')
                else:
                    self.speak_enabled = 'yes'
                    self.preferences.write(self.preference_file,
                                           'Speak',
                                           'speak_enabled',
                                           'yes')

            if self.speak_enabled == 'yes':
                self.speech.speak(voice, task)
            else:
                self.irc_socket.send('PRIVMSG ' + self.irc_channel + ' : ' + str(task) + '\r\n')

            del self.speak_tasks_array[0]

            return

    def chat_speak(self,
                   as_thread,
                   as_daemon,
                   conversation):
        """
        as_thread -> 'yes' if this method needs to be executed as a thread, 'no' if it doesn't
        as_daemon -> 'yes' if this method needs to be executed as a daemon, 'no' if it doesn't
        conversation -> (i.e 'Hello world') This text is meant as a raw IRC text parser. I strips the IRC stuff from it

        Takes a string from the think function and sends it to IRC

        :param as_thread:
        :param as_daemon:
        :param conversation:
        :return:
        """
        self.chat_speak_array.append(conversation)

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.thread.new_thread('yes',
                                       self.chat_speak_function)
            else:
                self.thread.new_thread('no',
                                       self.chat_speak_function)
        else:
            self.chat_speak_function()

    def chat_speak_function(self):

        """
        Executes the chat speak (the communication coming from others) if enabled as an inline object to main script

        :return:
        """
        for task in self.chat_speak_array:

            if task.find('toggleChatSpeak') != -1:
                if self.chat_speak_enabled == 'yes':
                    self.chat_speak_enabled = 'no'
                    self.preferences.write(self.preference_file,
                                           'Speak',
                                           'chat_speak_enabled',
                                           'no')
                else:
                    self.chat_speak_enabled = 'yes'
                    self.preferences.write(self.preference_file,
                                           'Speak',
                                           'chat_speak_enabled',
                                           'yes')

            #sentence = ''
            #try:
                # TODO Really!?! Find a better solutions. This is a bodge job. To specific!!!
            sentence = ((task.split(self.irc_channel)[1]).split(':')[1]).strip().replace("'", "\\'")
            #except:
                #pass

            if self.chat_speak_enabled == 'yes':
                self.speech.speak(self.irc_bot_voice, sentence)

            del self.chat_speak_array[0]

            return

    def act(self,
            as_thread,
            as_daemon,
            action,
            serial_port,
            baud_rate,
            time_out,
            action_parameter):
        """
        as_thread -> 'yes' if this method needs to be executed as a thread, 'no' if it doesn't
        as_daemon -> 'yes' if this method needs to be executed as a daemon, 'no' if it doesn't
        serial_port -> The serial port that it is given to be used
        baud_rate -> The baud_rate to be used
        time_out -> The serial port time out to be used
        action -> The name of the act action given in the Brain.csv file (i.e blink_pretty)
        action_parameter -> Place holder for secondary parameter None if there aren't any (i.e None)

        Takes a string from the think function converts it to an array and send it to act_function for execution.

        :param as_thread:
        :param as_daemon:
        :param serial_port:
        :param baud_rate:
        :param time_out:
        :param action:
        :param action_parameter:
        :return:
        """
        self.act_tasks_array.append([action, serial_port, baud_rate, time_out, action_parameter])

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.thread.new_thread('yes',
                                       self.act_function)
            else:
                self.thread.new_thread('no',
                                       self.act_function)
        else:
            self.act_function()

    def act_function(self):
        """
        Takes the act action from think function and passes it through to the skills class

        :return:
        """
        for task in self.act_tasks_array:

            exucute = ''\
                      + str(task[0]) + '.' + str(task[0])\
                      + '("' + str(task[1])\
                      + '", ' + str(task[2])\
                      + ', ' + str(task[3])\
                      + ', ' + str(task[4])\
                      + ')'

            exec exucute

            del self.act_tasks_array[0]

    def feel(self,
             as_thread,
             as_daemon,
             serial_port,
             baud_rate,
             time_out,
             action,
             action_parameter):
        """
        as_thread -> 'yes' if this method needs to be executed as a thread, 'no' if it doesn't
        as_daemon -> 'yes' if this method needs to be executed as a daemon, 'no' if it doesn't
        serial_port -> The serial port that it is given to be used
        baud_rate -> The baud_rate to be used
        time_out -> The serial port time out to be used
        action -> The name of the act action given in the Brain.csv file (i.e blink_pretty)
        action_parameter -> Place holder for secondary parameter None if there aren't any (i.e None)

        Takes a string from the think function converts it to an array and send it to feel_function for execution.

        :param as_thread:
        :param as_daemon:
        :param serial_port:
        :param baud_rate:
        :param time_out:
        :param action:
        :param action_parameter:
        :return:
        """
        self.feel_tasks_array.append([action, serial_port, baud_rate, time_out, action_parameter])

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.thread.new_thread('yes',
                                       self.feel_function)
            else:
                self.thread.new_thread('no',
                                       self.feel_function)
        else:
            self.feel_function()

    def feel_function(self):
        """
        Takes the feel action from think function and passes it through to the skills class (skills)

        :return:
        """
        for task in self.feel_tasks_array:

            exucute = ''\
                      + str(task[0]) + '.' + str(task[0])\
                      + '("' + str(task[1])\
                      + '", ' + str(task[2])\
                      + ', ' + str(task[3])\
                      + ', ' + str(task[4])\
                      + ')'

            exec exucute

            del self.feel_tasks_array[0]