__author__ = 'DeRaaf'
# TODO Clean up comments. Fix bugs. On going project!

import socket
from time import sleep

from Utilities import *

load_imports = Utilities()
load_imports.load_skills_init('skills/')
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
        irc_port -> Give the port number which IRC is using (i.e 6667)
        irc_channel -> Give the name of the IRC channel as quoted string (i.e '#FooChannel')
        irc_bot_nick -> Give a name to the IRC bot. This name needs to be same as you used for it's 'Brain'. But replace
                        underscores (_) with spaces if you use them (better not!). i.e the Brain.cvs is called
                        Robby_The_Robot.cvs the robot name has to be 'Robby the Robot'. Upper/lower cases are important!
        irc_bot_owner -> The name that you use as a IRC handle. Feature is handy when you want to invent something where
                         two bots battle in the name of it's owners or something

        # TODO buy some other physical devices (MSP or something) to see how this code can be made more universal
        physical_device_id -> The id of the physical device you connected (i.e arduino_1)
        serial_port_id -> The id of the serial device you created

        Set the IRC variables and create the IRC socket object

        Set the physical device variables

        :param irc_network:
        :param irc_port:
        :param irc_channel:
        :param irc_bot_nick:
        :param irc_bot_owner:
        :param physical_device_id:
        :param serial_port_id:
        """
        self.utility = Utilities()

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

        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.physical_device = physical_device_id

        self.serial_port = serial_port_id.serial_port
        self.baud_rate = serial_port_id.baud_rate
        self.time_out = serial_port_id.time_out

        self.start_thinking = False

        # self.utility.initiate_preference()

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

    def irc_connect(self):
        """
        Connect to give IRC channel

        :rtype : object
        """
        self.irc_socket.connect((self.irc_network, self.irc_port))
        if self.utility.get_preference_value('chat_log_enabled'):
            self.utility.create_chat_log(self.irc_bot_nick)
            self.utility.write_chat_log(self.irc_socket.recv(4096).strip()+'\n')
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
                self.utility.new_thread('yes', self.listen_function, 'none')
            else:
                self.utility.new_thread('no', self.listen_function, 'none')
        else:
            self.listen_function()

    def listen_function(self):
        """
        Puts the individual IRC conversation in a task list so the think function can handle it one 'thought' at a time.

        :return:
        """
        self.get_born()
        while True:
            conversation = self.irc_socket.recv(4096)
            if conversation.find('PING') != -1:
                self.survive(conversation)
            else:
                if conversation:
                    sleep(0.2)
                    cleaned_conversation = self.utility.parse_irc_chat(conversation)

                    # TODO Need some way's to do some fun stuff with this!
                    # print(cleaned_conversation[0])
                    # print(cleaned_conversation[1])
                    # print(' '.join(cleaned_conversation[2]))
                    # print(cleaned_conversation[3])

                    self.think('no', 'no', [cleaned_conversation[0], cleaned_conversation[3]])

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
        # Put the received conversation into the thinking task array
        self.think_tasks_array.append(conversation)

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.utility.new_thread('yes', self.think_function, 'none')
            else:
                self.utility.new_thread('no', self.think_function, 'none')
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
        # Loop through the thinking task array
        for task in self.think_tasks_array:

            # Send the sentence received to a utility that check for the keyword to toggle chat on/off
            if self.utility.set_toggle_state(str(task[1]), self.irc_bot_nick, 0):
                self.irc_socket.send('PRIVMSG '
                                     + self.irc_channel
                                     + ' : Log chat : '
                                     + self.utility.get_preference_value('chat_log_enabled')
                                     + '\r\n')

            # Send the sentence received to a utility that check for the keyword to toggle voice on/off
            if self.utility.set_toggle_state(str(task[1]), self.irc_bot_nick, 1):
                self.irc_socket.send('PRIVMSG '
                                     + self.irc_channel
                                     + ' : Voice  : '
                                     + self.utility.get_preference_value('voice_enabled')
                                     + '\r\n')

            # Send the sentence received to a utility that check for the keyword to toggle chat on/off
            if self.utility.set_toggle_state(str(task[1]), self.irc_bot_nick, 2):
                self.irc_socket.send('PRIVMSG '
                                     + self.irc_channel
                                     + ' : Chat voice  : '
                                     + self.utility.get_preference_value('chat_voice_enabled')
                                     + '\r\n')

            # Send the sentence received to a utility that check for the keyword to toggle chat on/off
            if self.utility.set_toggle_state(str(task[1]), self.irc_bot_nick, 3):
                self.irc_socket.send('PRIVMSG '
                                     + self.irc_channel
                                     + ' : Nick voice : '
                                     + self.utility.get_preference_value('announcement_voice_enabled')
                                     + '\r\n')

            # If chat logging is enabled write the sentence to the file
            if self.utility.get_preference_value('chat_log_enabled') == 'yes':
                self.utility.write_chat_log(task)
            else:
                pass

            # Only start 'thinking' if al the header information from the IRC is received (otherwise headache!)
            if task[1].find('End of /NAMES list') != -1:
                if not self.start_thinking:
                    self.start_thinking = True

            # Start the 'thinking' function
            if self.start_thinking:

                self.chat_speak('no', 'no', task)

                # Little bit of a hackish solution to deal with empty strings coming from the IRC. It works for now
                execute = self.utility.check_conversation(task[1], self.irc_bot_nick)

                if execute:

                    # TODO Scaffolding code for what to do with directed messages
                    if execute[1] == 'yes':
                        pass

                    self.speak('yes', 'no', execute[2], execute[3])

                    # If a message is received that calls for an serial action
                    if execute[7] != 'no':
                        self.act('yes', 'no', execute[7], self.serial_port, self.baud_rate, self.time_out, execute[8])

                    # If a message is received that calls for to listen to a serial function
                    if execute[4] != 'no':
                        self.feel('yes', 'no', execute[4], self.serial_port, self.baud_rate, self.time_out, execute[5])

            # Clear this thinking task from the array
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
        # Put the conversation received into the speak_task_array
        self.speak_tasks_array.append(conversation)

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.utility.new_thread('yes', self.speak_function, voice)
            else:
                self.utility.new_thread('no', self.speak_function, voice)
        else:
            self.speak_function(voice)

    def speak_function(self,
                       voice):
        """
        voice -> A voice name used on Mac OSX system as a quoted string. Gets passed from Brain.csv (i.e 'Alex')

        Executes the speak function (the communication coming from itself) if enabled as an parallel (threaded)
        object to main script

        :param voice:
        :return:
        """
        # TODO Implement code in Utilities
        for task in self.speak_tasks_array:

            if self.utility.get_preference_value('voice_enabled') == 'yes':
                self.irc_socket.send('PRIVMSG ' + self.irc_channel + ' : ' + str(task) + '\r\n')
                if self.utility.get_preference_value('chat_log_enabled') == 'yes':
                    self.utility.write_chat_log(['RESPONSE -> ' + self.irc_bot_nick, str(task) + '\r\n'])
                else:
                    pass
                self.utility.speak(voice, task)
            else:
                self.irc_socket.send('PRIVMSG ' + self.irc_channel + ' : ' + str(task) + '\r\n')
                if self.utility.get_preference_value('chat_log_enabled') == 'yes':
                    self.utility.write_chat_log(['RESPONSE -> ' + self.irc_bot_nick, str(task) + '\r\n'])
                else:
                    pass

            # Remove task from the speak task array
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
        # Put chat speak task in the speak chat array
        self.chat_speak_array.append(conversation)

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.thread.new_thread('yes', self.chat_speak_function)
            else:
                self.thread.new_thread('no', self.chat_speak_function)
        else:
            self.chat_speak_function()

    def chat_speak_function(self):

        """
        Executes the chat speak (the communication coming from others) if enabled as an inline object to main script

        :return:
        """
        for task in self.chat_speak_array:

            if self.utility.get_preference_value('announcement_voice_enabled') == 'yes':
                nick_speaker = task[0].split('!')
                self.utility.speak(self.utility.get_preference_value('announcement_voice'), str(nick_speaker[0]))
                sleep(0.15)
            else:
                pass
            if self.utility.chat_voice_enabled == 'yes':
                speakers_sentence = task[1]
                sleep(0.6)
                # TODO make voice IRC user selectable would be a nice feature!!
                self.utility.speak(self.utility.get_preference_value('voice'), speakers_sentence)

            # Remove task form array
            del self.chat_speak_array[0]

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
        # Put task inside act tasks array
        self.act_tasks_array.append([action, serial_port, baud_rate, time_out, action_parameter])

        if as_thread == 'yes':
            if as_daemon == 'yes':
                self.utility.new_thread('yes', self.act_function)
            else:
                self.utility.new_thread('no', self.act_function)
        else:
            self.act_function()

    def act_function(self):
        """
        Takes the act action from think function and passes it through to the skills class

        :return:
        """
        for task in self.act_tasks_array:

            execute = ''\
                      + str(task[0]) + '.' + str(task[0])\
                      + '("' + str(task[1])\
                      + '", ' + str(task[2])\
                      + ', ' + str(task[3])\
                      + ', ' + str(task[4])\
                      + ')'

            exec execute

            # Remove the act task from the array
            del self.act_tasks_array[0]

    def feel(self,
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
                self.utility.new_thread('yes', self.feel_function)
            else:
                self.utility.new_thread('no', self.feel_function)
        else:
            self.feel_function()

    def feel_function(self):
        """
        Takes the feel action from think function and passes it through to the skills class (skills)

        :return:
        """
        for task in self.feel_tasks_array:

            # TODO double code!

            execute = ''\
                      + str(task[0]) + '.' + str(task[0])\
                      + '("' + str(task[1])\
                      + '", ' + str(task[2])\
                      + ', ' + str(task[3])\
                      + ', ' + str(task[4])\
                      + ')'

            exec execute

            del self.feel_tasks_array[0]