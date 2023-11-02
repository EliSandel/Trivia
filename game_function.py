

def check_answer(self, answer):
    player_answer = self.buttons[answer]['text']
    if player_answer == self.all_questions[self.counter]['correct_answer']:
        self.correct_answer()
    else:
        self.wrong_answer()
    
    self.counter += 1
    self.next_question()
        
        

