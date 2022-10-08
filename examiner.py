from random import randint

from triviaPersistenceManager import TriviaPersistenceManager

class Examiner:
    data_manager = TriviaPersistenceManager()
    questions = {}
    questions_order = []
    questions_amount = 0
    answered_questions = 0
    points_gained = 0
    answers = {}

    def get_questions(self):
        self.questions = self.data_manager.get_questions()

    def get_answers(self, verbal_time_key):
        self.answers = self.data_manager.get_answers(verbal_time_key)
    
    def shuffle_questions(self):
        self.questions_amount = len(self.questions)
        questions_index_dict = {}
        for index in range (0, self.questions_amount):
            questions_index_dict[index] = 0
        for counter in range (0, self.questions_amount):
            question_index = randint(0, 9)
            while questions_index_dict[question_index]:
                question_index = (question_index + 1) % self.questions_amount
            self.questions_order.append(question_index)
            questions_index_dict[question_index] = 1

    def validate_answer(self, question_index, answer):
        correctness = False
        answer = answer.strip().lower()
        if answer == self.answers[ str(self.questions_order[question_index] + 1) ]:
            correctness = True
        return correctness
    
    def prepare_data(self, verbal_time_key):
        self.get_questions()
        self.get_answers(verbal_time_key)
        self.answered_questions = 0
        self.points_gained = 0

    def quiz(self, verbal_time_key):
        self.prepare_data(verbal_time_key)
        self.shuffle_questions()

    def is_game_over(self):
        game_over = False
        if self.answered_questions == self.questions_amount:
            game_over = True
        return game_over
    
    def get_next_question(self):
        return self.questions[ str(self.questions_order[ self.answered_questions ] + 1) ]
    
    def answer_current_question(self, answer):
        correctness = self.validate_answer(self.answered_questions, answer)
        if correctness == True:
            self.points_gained += 1
        self.answered_questions += 1
        return correctness

    def get_points(self): 
        return self.points_gained
