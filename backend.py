import question_data

class Backend():
    def __init__(self, server):
        self.server = server
        self.turn_counter = 0
        self.score = [0, 0]  #assuming two players
        self.amount_of_players_answered = 0
        self.trivia_api = question_data.TriviaApi()
        self.data = self.trivia_api.get_trivia_questions()
        
    def check_answer(self, player, answer):
        if answer == self.data[self.turn_counter]['correct_answer']:
            self.correct_answer(player)
        self.amount_of_players_answered += 1
        if self.amount_of_players_answered == 2:
            self.amount_of_players_answered = 0
            self.turn_counter += 1
            if self.turn_counter == len(self.data) + 1:#when i run the test try without +1
                self.game_over()

    def correct_answer(self, player):
        self.score[player] += 1

    def next_question(self):
        question = self.data[self.turn_counter]
        return question

    def get_score(self, player):
        return self.score[player]
    
    def game_over(self):
        highest_score = max(self.score) 
        winners = [player for player, score in enumerate(self.score) if score == highest_score]
        self.server.game_over(winners)
        
