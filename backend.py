import question_data

class Backend():
    def __init__(self):
        self.turn_counter = 0
        self.score = [0, 0]  #assuming two players
        self.trivia_api = question_data.TriviaApi()
        self.data = self.trivia_api.get_trivia_questions()
        self.next_question()
        
    def check_answer(self, player, answer):
        if answer == self.data[self.turn_counter]['correct_answer']:
            self.correct_answer(player)

    def correct_answer(self, player):
        self.score[player] += 1

    def next_question(self):
        question = self.data[self.turn_counter]
        self.turn_counter += 1
        return question

    def get_score(self, player):
        return self.score[player]
        
