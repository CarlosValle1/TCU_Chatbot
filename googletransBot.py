from googletrans import Translator

class GoogletransBot(Translator):

    spanish = 'es'
    english = 'en'

    def translate_text(self, rawMsg):
        lang = self.detect(rawMsg).lang
        response = ""
        if lang == self.english:
            response = self.translate(rawMsg, src = self.english, dest = self.spanish).text
        else:
            response = self.translate(rawMsg, src = self.spanish, dest = self.english).text
        return response
        