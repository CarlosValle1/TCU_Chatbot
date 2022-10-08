from dataPersistenceManager import DataPersistenceManager

class TriviaPersistenceManager(DataPersistenceManager):
    def get_questions(self):
        question_dict = {}
        questions = self.get_data('questions')
        for question in questions:
            question_dict[question['id']] = question['text']
        return question_dict

    def get_answers(self, verbal_time):
        answers_dict = {}
        all_answers_group = self.get_data('answers')
        for answer_group in all_answers_group:
            if answer_group['id'] == verbal_time:
                for answer in answer_group['answers']:
                    answers_dict[answer['id']] = answer['text']
                break
        return answers_dict

