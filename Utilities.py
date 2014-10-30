__author__ = 'DeRaaf'
# TODO Clean up comments. Fix bugs. On going project!

import os
from os import system
import sys
import ConfigParser
import threading
import csv
import time


class Utilities (object):

    def __init__(self):
        self.preference_parser = ConfigParser.RawConfigParser()
        self.thread = threading.Thread()

        self.preference_file = 'pref/preferences.txt'

        self.initiate_preference()

        self.chat_log_enabled = self.read_preference('Log Settings', 'chat')

        self.voice_enabled = self.read_preference('Speak', 'voice_enabled')
        self.chat_voice_enabled = self.read_preference('Speak', 'chat_voice_enabled')
        self.announcement_voice_enabled = self.read_preference('Speak', 'announcement_voice_enabled')

        self.voice = self.read_preference('Voices', 'default')
        self.chat_voice = self.read_preference('Voices', 'chat_voice')
        self.announcement_voice = self.read_preference('Voices', 'announcement_voice')

        self.chat_directory = 'logs/chat/'
        self.timestamp = time.strftime('%m%d%Y%H%M')
        self.chat_log_file = ''

    def __str__(self):
        return '\n\nCallable methods:\n\n' \
               '.initiate_preferences : Creates a preference file\n' \
               '.read_preferences : Reads from preferences file\n' \
               '.write_preferences : Write to preferences file' \
               '.get_preference_value : Get the value for a variable' \
               '' \
               '\n\n'.format()

    def __getattr__(self):
        return '{0}'.format('Not Found')

    def initiate_preference(self):
        """
        Creates a preference file (i.e. .initiate("pref/preferences.txt"))

        :return:
        """
        if os.path.exists(self.preference_file):
            pass
        else:
            temp_file = open(self.preference_file, 'w+')

            self.preference_parser.add_section('Speak')
            self.preference_parser.set('Speak', 'voice_enabled', 'yes')
            self.preference_parser.set('Speak', 'chat_voice_enabled', 'yes')
            self.preference_parser.set('Speak', 'announcement_voice_enabled', 'yes')

            self.preference_parser.add_section('Voices')
            self.preference_parser.set('Voices', 'default', 'Zarvox')
            self.preference_parser.set('Voices', 'chat_voice', 'Alex')
            self.preference_parser.set('Voices', 'announcement_voice', 'Whisper')

            self.preference_parser.add_section('Log Settings')
            self.preference_parser.set('Log Settings', 'chat', 'yes')
            self.preference_parser.write(open(self.preference_file, 'w'))

            temp_file.close()

    def read_preference(self, session, key):
        """
        preference_file -> file to read/write from/to (i.e 'pref/preferences.txt')
        section -> Which section of preferences (i.e 'Speech')
        key -> Which key of preferences (i.e 'speech_enabled')

        Reads from preferences file (i.e. .read("pref/preferences.txt", "section", "key"))

        :param session:
        :param key:
        :return:
        """
        temp_file = open(self.preference_file, 'r')
        self.preference_parser.readfp(temp_file)
        temp_value = self.preference_parser.get(session, key)
        temp_file.close()
        return temp_value

    def write_preference(self, session, key, value):
        """
        preference_file -> file to read/write from/to (i.e 'pref/preferences.txt')
        section -> Which section of preferences (i.e 'Speech')
        key -> Which key of preferences (i.e 'speech_enabled')
        value -> The value to be writen (i.e 'yes')

        Write to preferences file (i.e .write("pref/preferences.txt", "section", "key", "value"))

        :param session:
        :param key:
        :param value:
        :return:
        """
        temp_file = open(self.preference_file, 'r')
        self.preference_parser.readfp(temp_file)
        self.preference_parser.set(session, key, value)
        self.preference_parser.write(open(self.preference_file, 'w'))
        temp_file.close()

    def get_preference_value(self, preference):
        """
        preference ->  Value to return

        These can be returned
        'chat_log_enabled'
        'voice_enabled'
        'chat_voice_enabled'
        'announcement_voice_enabled'

        :param preference:
        :return:
        """
        if preference == 'chat_log_enabled':
            return self.chat_log_enabled

        if preference == 'voice_enabled':
            return self.voice_enabled
        if preference == 'chat_voice_enabled':
            return self.chat_voice_enabled
        if preference == 'announcement_voice_enabled':
            return self.announcement_voice_enabled

        if preference == 'voice':
            return  self.voice
        if preference == 'chat_voice':
            return self.chat_voice
        if preference == 'announcement_voice':
            return self.announcement_voice

    def create_chat_log(self, irc_bot_name):
        """
        irc_bot_name -> The name of the IRCBot

        This creates a new chat log file for every session started

        :param irc_bot_name:
        :return:
        """
        if self.chat_log_enabled == 'yes':
            if not os.path.exists(self.chat_directory):
                os.makedirs(self.chat_directory, mode=0755)
            self.chat_log_file = str(irc_bot_name + '.' + self.timestamp+'.txt')
        else:
            pass

    def write_chat_log(self, sentence):
        """
        sentence -> String send from the IRCBot to log

        Write to the chat log

        :param sentence:
        :return:
        """
        if self.chat_log_enabled == 'yes':
            log_file = open((self.chat_directory + self.chat_log_file), "a")  # chat log file
            log_file.write(str(sentence[0] + ' : ' + sentence[1]))
        else:
            pass

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
        else:
            pass

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
        sentence -> Takes parsed (or raw) IRC communication and check it against the Brains.csv file
        irc_bot_name -> Helps if you want multiple IRCBots Walking around

        Check a cerain string against the Brin.csv

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

    def set_toggle_state(self, sentence, irc_bot_nick, check):
        """
        sentence -> The sentence to check
        irc_the_nick -> For which IRCBot is this test
        check -> What to test takes in a number (i.e 1)

        check [0] -> Chat log
        check [1] -> IRCBot speech
        check [2] -> Chat room speech
        check [3] -> Nick announecement

        :param sentence:
        :param irc_bot_nick:
        :param check:
        """
        checks_array = [['.toggleChatLog', self.chat_log_enabled, 'Log Settings', 'chat'],
                        ['.toggleVoice', self.voice_enabled, 'Speak', 'speak_enabled'],
                        ['.toggleChatVoice', self.chat_voice_enabled, 'Speak', 'chat_speak_enabled'],
                        ['.toggleNickVoice', self.announcement_voice_enabled, 'Speak', 'announcement_speak_enabled']]

        if sentence.find(irc_bot_nick + checks_array[check][0]) != -1:
            if self.get_preference_value(checks_array[check][1]) == 'yes':
                self.write_preference(checks_array[check][2], checks_array[check][3], 'no')
                return True
            if self.get_preference_value(checks_array[check][1]) == 'no':
                self.write_preference(checks_array[check][2], checks_array[check][3], 'yes')
                return True
        else:
            return False

    def load_skills_init(self, path_to_skills):
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