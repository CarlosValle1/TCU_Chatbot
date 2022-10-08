from typing import Dict
import requests
import json

class OxfordDictionary():
    APP_ID = 'bc2b63ae'
    APP_KEY = '900b6c2606e09bb2429ef330fc142099'
    LANGUAGE = 'en-us'
    BASE_URL = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + LANGUAGE + '/'
    last_word_consulted = ''
    filtered_dictionary = {}

    def query_word(self, word: str):
        url = self.BASE_URL + word.lower()
        response = requests.get(url, headers={'app_id': self.APP_ID, 'app_key': self.APP_KEY})
        response_as_dictionary = json.loads(response.text)
        return response_as_dictionary

    def filter_response_dictionary(self, response_as_dictionary):
        self.filtered_dictionary = {}
        if 'error' in response_as_dictionary:
            self.filtered_dictionary['error'] = response_as_dictionary['error']
            return self.filtered_dictionary
        senses = response_as_dictionary['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
        self.filtered_dictionary['main_definition'] = senses[0]['definitions'][0]
        if 'example' in senses[0]:
            self.filtered_dictionary['main_example'] = senses[0]['examples'][0]['text']
        else:
            self.filtered_dictionary['main_example'] = ''

        self.filtered_dictionary['secondary_data'] = {}
        if 'subsenses' in senses[0]:
            subsenses = senses[0]['subsenses']
            self.filtered_dictionary['secondary_data']['definitions'] = []
            self.filtered_dictionary['secondary_data']['examples'] = []
            secondary_definitions_total = len(subsenses)
            for counter in range(0, secondary_definitions_total):
                if 'definitions' not in senses[0]['subsenses'][counter]:
                    break
                self.filtered_dictionary['secondary_data']['definitions'].append(subsenses[counter]['definitions'][0])
                if 'examples' in senses[0]['subsenses'][counter]:
                    self.filtered_dictionary['secondary_data']['examples'].append(subsenses[counter]['examples'][0]['text'])
                else:
                    self.filtered_dictionary['secondary_data']['examples'].append('no_example')

    def consult_word(self, word: str):
        self.filter_response_dictionary( self.query_word(word) )
        self.last_word_consulted = word

    def get_main_definition(self, word:str):
        if word != self.last_word_consulted:
            self.consult_word(word)
        if 'error' in self.filtered_dictionary:
            return { 'error': self.filtered_dictionary['error'] }
        return { 'main_definition': self.filtered_dictionary['main_definition'] }

    def get_main_example(self, word: str):
        if word != self.last_word_consulted:
            self.consult_word(word)
        if 'error' in self.filtered_dictionary:
            return { 'error': self.filtered_dictionary['error'] }
        return { 'main_example': self.filtered_dictionary['main_example'] }

    def get_main_definition_and_example(self, word: str):
        if word != self.last_word_consulted:
            self.consult_word(word)
        if 'error' in self.filtered_dictionary:
            return { 'error': self.filtered_dictionary['error'] }
        return {
            'main_definition': self.filtered_dictionary['main_definition'],
            'main_example': self.filtered_dictionary['main_example']
            }

    def get_secondary_definitions_and_examples(self, word:str):
        if word != self.last_word_consulted:
            self.consult_word(word)
        if 'error' in self.filtered_dictionary:
            return { 'error': self.filtered_dictionary['error'] }
        return self.filtered_dictionary['secondary_data']
