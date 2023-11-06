import question_data

class Backend():
    def __init__(self, server, player_names):
        self.server = server
        self.player_names = player_names
        self.turn_counter = 0
        self.scores = []  
        self.trivia_api = question_data.TriviaApi()
        self.data = self.trivia_api.get_trivia_questions()
        
    def check_answer(self, array_of_answers): #array of answers
        for player_index,answer in enumerate(array_of_answers):
            if answer == self.data[self.turn_counter]['correct_answer']:
                self.correct_answer(player_index)
        self.turn_counter += 1

    def correct_answer(self, player):
        self.scores[player] += 1

    def next_question(self):
        question = self.data[self.turn_counter]
        return question

    def get_score(self): #return the array
        # if self.turn_counter == len(self.data) + 1:#when i run the test try without +1
        #     self.game_over()
        # else:
        return self.scores
    
    def game_over(self):
        highest_score = max(self.scores) 
        winners = [player for player, scores in enumerate(self.scores) if scores == highest_score]
        self.server.game_over(winners)
        
