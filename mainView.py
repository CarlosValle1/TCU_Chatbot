from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

import datetime
from examiner import Examiner
from enum import Enum

from oxfordDictionary import OxfordDictionary

class ConversationStatus(Enum):
    NORMAL = 0
    PRE_GAME = 1
    IN_GAME = 2

class Ui(ScreenManager):
    dictionaryBot = OxfordDictionary()
    examiner = Examiner()
    status = ConversationStatus.NORMAL

    def add_bot_msg(self, msg):
        currentime = datetime.datetime.now()
        time = currentime.strftime('%H:%M')
        msg = msg.strip()
        new_card = BotMsgTextCard(text = msg, dateTime = time)
        self.ids.chatCanvas.add_widget(new_card)
    
    def add_user_msg(self, msg):
        currentime = datetime.datetime.now()
        time = currentime.strftime('%H:%M')
        msg = msg.strip()
        new_card = UserMsgTextCard(text = msg, dateTime = time)
        self.ids.chatCanvas.add_widget(new_card)

    def user_sent_message_event(self, widget):
        widget_text_stripped = widget.text.strip()
        if widget_text_stripped:
            self.add_user_msg(widget_text_stripped)
            widget.text = ''
            self.message_sent_protocol(widget_text_stripped)

    def message_sent_protocol(self, msg):
        if self.is_it_a_command(msg):
            self.command_handling_protocol(msg)
        else:
            if self.status == ConversationStatus.IN_GAME:
                self.play_question(msg)
            else:
                self.define_word(msg)

    def is_it_a_command(self, msg):
        answer = False
        if msg and msg[0] == '/':
            answer = True
        return answer

    def command_handling_protocol(self, command):
        command = command[1:].lower()
        match command:
            case 'play':
                self.play_command_protocol()
            case 'past simple':
                self.verbal_time_command_protocol('past_simple')
            case 'past continuous':
                self.verbal_time_command_protocol('past_continuous')
            case 'past perfect simple':
                self.verbal_time_command_protocol('past_perfect_simple')
            case 'past perfect continuous':
                self.verbal_time_command_protocol('past_perfect_continuous')
            case 'present simple':
                self.verbal_time_command_protocol('present_simple')
            case 'present continuous':
                self.verbal_time_command_protocol('present_continuous')
            case 'present perfect simple':
                self.verbal_time_command_protocol('present_perfect_simple')
            case 'present perfect continuous':
                self.verbal_time_command_protocol('present_perfect_continuous')
            case 'future simple':
                self.verbal_time_command_protocol('future_simple')
            case 'future continuous':
                self.verbal_time_command_protocol('future_continuous')
            case 'future perfect simple':
                self.verbal_time_command_protocol('future_perfect_simple')
            case 'future perfect continuous':
                self.verbal_time_command_protocol('future_perfect_continuous')
            case 'quit':
                self.quit_command_protocol()
            case other:
                self.add_bot_msg("Oops, I don't know what /" + other + " is. Check the instructions to find available commands!")

    def play_command_protocol(self):
        if self.status == ConversationStatus.NORMAL:
            self.status = ConversationStatus.PRE_GAME
            self.add_bot_msg("Ok, let's play, you better be ready!")
            self.add_bot_msg("Firstly, choose the verbal time with the correct command")
            self.add_bot_msg('If you are doubtful of the possible commands, check the game instructions')
        else:
            self.add_bot_msg('We are in the middle of a game right now!')
            self.add_bot_msg('Type "/quit" to end the current game, and then we can start another')

    def verbal_time_command_protocol(self, command):
        if self.status == ConversationStatus.PRE_GAME:
            self.status = ConversationStatus.IN_GAME
            self.examiner.quiz(command)
            self.add_bot_msg('QUESTION: ' + self.examiner.get_next_question()) # send first question
        elif self.status == ConversationStatus.NORMAL:
            self.add_bot_msg('Ups, we are not in a game right now!')
            self.add_bot_msg('Type "/play" to start a new game and then specify a verbal time')
        elif self.status == ConversationStatus.IN_GAME:
            self.add_bot_msg('We are in the middle of a game right now!')
            self.add_bot_msg('Type "/quit" to end the current game, and then "/play" to start another')

    def quit_command_protocol(self):
        if self.status == ConversationStatus.PRE_GAME or self.status == ConversationStatus.IN_GAME:
            self.status = ConversationStatus.NORMAL
            self.add_bot_msg("Ok, let's call the game over!")
        else:
            self.add_bot_msg('We are not in game, everything ok!')

    def play_question(self, answer):
        self.examiner.answer_current_question(answer)
        if not self.examiner.is_game_over():
            self.add_bot_msg('QUESTION: ' + self.examiner.get_next_question())
        else:
            self.add_bot_msg('The game is over! You got ' + str(self.examiner.get_points()) + ' points.')
            self.status = ConversationStatus.NORMAL

    def define_word(self, msg):
        if 'error' in self.dictionaryBot.get_main_definition(msg):
            self.add_bot_msg(self.dictionaryBot.get_main_definition(msg)['error'])
        else:
            main_definition = self.dictionaryBot.get_main_definition(msg)['main_definition']
            self.add_bot_msg('MAIN DEFINITION:')
            self.add_bot_msg(main_definition)
            main_example = self.dictionaryBot.get_main_example(msg)['main_example']
            if main_example != 'no_example':
                self.add_bot_msg('Main example: ' + main_example)
            secondary_data = self.dictionaryBot.get_secondary_definitions_and_examples(msg)
            if 'definitions' in secondary_data:
                for i in range(0, len(secondary_data['definitions'])):
                    self.add_bot_msg('Secondary definition: ' + secondary_data['definitions'][i])
                    if secondary_data['examples'][i] != 'no_example':
                        self.add_bot_msg('Secondary example: ' + secondary_data['examples'][i])
            
class ChatTextCard(MDCard):
    pass

class BotMsgTextCard(ChatTextCard):
    pass

class UserMsgTextCard(ChatTextCard):
    pass

class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('mainDesign.kv')
        return Ui()