import json

class PersistenceManager:
    data_path = './data/'
    questions_file_path = data_path + 'questions.json'
    answers_file_path = data_path + 'answers.json'

    def get_questions(self):
        question_dict = {}
        with open(self.questions_file_path, 'r') as questions_file:
            questions_as_json = json.load(questions_file)
            for question in questions_as_json:
                question_dict[question['id']] = question['text']
        return question_dict

    def get_answers(self, verbal_time):
        answers_dict = {}
        with open(self.answers_file_path, 'r') as answers_file:
            all_answers_as_json = json.load(answers_file)
            for answer_group in all_answers_as_json:
                if answer_group['id'] == verbal_time:
                    for answer in answer_group['answers']:
                        answers_dict[answer['id']] = answer['text']
                    break
        return answers_dict
