__author__ = 'DeRaaf'
# TODO Clean up comments. Fix bugs. On going project!

import os
from os import system
import sys
import ConfigParser
import threading
import csv


class Utilities (object):

    def __init__(self):
        self.parser = ConfigParser.RawConfigParser()
        self.thread = threading.Thread()

    def __str__(self):
        return '\n\nCallable methods:\n\n' \
               '.initiate : Creates a preference file (i.e. .iniate("pref/preferences.txt"))\n' \
               '.read : Reads from preferences file (i.e. .read("pref/preferences.txt", "section", "key"))\n' \
               '.write : Write to preferences file (i.e .write("pref/preferences.txt", "section", "key", "value"))' \
               '\n\n'.format()

    def __getattr__(self):
        return '{0}'.format('Not Found')

    def initiate(self,
                 preference_file):
        """
        preference_file -> file to read/write from/to (i.e 'pref/preferences.txt')

        Creates a preference file (i.e. .initiate("pref/preferences.txt"))

        :param preference_file:
        :return:
        """
        if os.path.exists(preference_file):
            return True
        else:
            # If there is no preference file yet create one with these default settings
            temp_file = open(preference_file, 'w+')
            #preference_parser.readfp(temp_file)
            self.parser.add_section('Speak')
            self.parser.set('Speak', 'speak_enabled', 'yes')
            self.parser.set('Speak', 'chat_speak_enabled', 'yes')
            self.parser.set('Speak', 'announcement_speak_enabled', 'yes')
            self.parser.add_section('Voices')
            self.parser.set('Voices', 'default', 'Zarvox')
            self.parser.set('Voices', 'irc_announcement_voice', 'Whisper')
            self.parser.add_section('Log Settings')
            self.parser.set('Log Settings', 'chat', 'yes')
            self.parser.write(open(preference_file, 'w'))
            temp_file.close()

    def read(self,
             preference_file,
             session,
             key):
        """
        preference_file -> file to read/write from/to (i.e 'pref/preferences.txt')
        section -> Which section of preferences (i.e 'Speech')
        key -> Which key of preferences (i.e 'speech_enabled')

        Reads from preferences file (i.e. .read("pref/preferences.txt", "section", "key"))

        :param preference_file:
        :param session:
        :param key:
        :return:
        """
        temp_file = open(preference_file, 'r')
        self.parser.readfp(temp_file)
        temp_value = self.parser.get(session, key)
        temp_file.close()
        return temp_value

    def write(self,
              preference_file,
              session,
              key,
              value):
        """
        preference_file -> file to read/write from/to (i.e 'pref/preferences.txt')
        section -> Which section of preferences (i.e 'Speech')
        key -> Which key of preferences (i.e 'speech_enabled')
        value -> The value to be writen (i.e 'yes')

        Write to preferences file (i.e .write("pref/preferences.txt", "section", "key", "value"))

        :param preference_file:
        :param session:
        :param key:
        :param value:
        :return:
        """
        temp_file = open(preference_file, 'r')
        self.parser.readfp(temp_file)
        self.parser.set(session, key, value)
        self.parser.write(open(preference_file, 'w'))
        temp_file.close()

    def new_thread(self,
                   as_daemon,
                   function,
                   *parameters):
        """
        as_daemon -> Yes if a function needs to be a Daemon process or not
        function -> The name of the function passed through from Brain.csv
        parameters -> The parameters the function needs

        :param as_daemon:
        :param function:
        :param parameters:
        """
        if as_daemon == 'yes':
            self.thread.daemonSet = True
            self.thread.__init__(target=function, name=str(function), args=parameters)
            self.thread.start()
            # self.thread.join()
        else:
            self.thread.__init__(target=function, name=str(function), args=parameters)
            self.thread.start()
            # self.thread.join()

    def speak(self, voice, sentence):
        """
        voice -> Name of the Mac OS X voice to be used (i.e Alex)

        :param voice:
        :param sentence:
        """
        if 'darwin' in sys.platform:
            if voice:
                system('say -v ' + voice + ' ' + sentence)
            else:
                system('say ' + sentence)

    def parse_irc_chat(self, sentence):
        """
        sentence -> Raw IRC strings
        type_of_return -> 'all' give back a tuple with all eh IRC info. text_only gives back senteces
        Takes in the raw string from the IRC chat and converts it to something more manageable
        :param sentence:
        :return:
        """
        irc_prefix = ''
        irc_trailing = ''
        if sentence.startswith(':'):
            irc_prefix, sentence = sentence[1:].split(' ', 1)
        if ' :' in sentence:
            sentence, irc_trailing = sentence.split(' :', 1)
        irc_arguments = sentence.split()
        return irc_prefix, irc_arguments.pop(0), irc_arguments, irc_trailing

    def check_conversation(self, sentence, irc_bot_name):
        """
        sentence -> Takes 'raw' IRC communication and check it against the Brains.csv file
        irc_bot_name -> Helps if you want multiple IRCBots Walking around

        :param sentence:
        :param irc_bot_name:
        :return:
        """
        where_is_my_brain = os.path.join((os.getcwd()), 'brains', irc_bot_name.replace(' ', '_'), 'Brain.csv')
        with open(where_is_my_brain, 'rb') as brain:
            dialect = csv.Sniffer().sniff(brain.read(1024),
                                          delimiters=';,')
            brain.seek(0)
            deep_thoughts = csv.reader(brain,
                                       dialect)
            for thought in deep_thoughts:
                if sentence.lower().find(thought[0]) != -1:
                    return thought