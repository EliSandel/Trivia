import question_data
import random

class Backend():
    def __init__(self, server):
        self.server = server
        self.player_names = ""
        self.turn_counter = 0
        self.scores = []  
        self.trivia_api = question_data.TriviaApi()
        self.data = self.trivia_api.get_trivia_questions()
        
    def check_answer(self, array_of_answers): #array of answers
        for player_index,answer in enumerate(array_of_answers):
            if answer == self.data[self.turn_counter]['correct_answer']:
                self.correct_answer(player_index)
        self.turn_counter += 1

    def correct_answer(self, player_index):
        self.scores[player_index] += 1

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
        
    def initiate_score_list(self):
        print(self.player_names)
        for player in self.player_names:
            self.scores.append(0)
    
    def generate_random_room_id(self, array):
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in array:
                return new_id
            
    def get_list_of_names(self, names):
        self.player_names = names
        self.initiate_score_list()

        
