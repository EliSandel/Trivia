import tkinter as tk
from functools import partial 
import test
import json

class GameGraphics:
    def __init__(self, root):
        self.root = root
        self.counter = 0
        self.score = 0
        
        self.gui_setup()
        
    def gui_setup(self):
        self.root.title("Trivia")
        self.root.config(padx=50, pady=50, bg="white")
        
        self.score_label = tk.Label(text="score")
        self.opponent_score_label = tk.Label(text="opponent score")
        self.question_label = tk.Label(text="question")
        self.buttons = {}
        self.buttons['a'] = tk.Button(text="a", command=partial(self.send_answer, 'a'))
        self.buttons['b'] = tk.Button(text="b", command=partial(self.send_answer, 'b'))
        self.buttons['c'] = tk.Button(text="c", command=partial(self.send_answer, 'c'))
        self.buttons['d'] = tk.Button(text="d", command=partial(self.send_answer, 'd'))
        
        self.score_label.grid(row=0, column=0)
        self.opponent_score_label.grid(row=0, column=2)
        self.question_label.grid(row=1, column=1)
        self.buttons['a'].grid(row=2, column=1)
        self.buttons['b'].grid(row=3, column=1)
        self.buttons['c'].grid(row=4, column=1)
        self.buttons['d'].grid(row=5, column=1)
        


        
    def next_question(self, data):
        print(type(data))
        data = data.replace("'",'"')
        data = json.loads(data)
        print(type(data))
        self.question_label.config(text=data['question'])
        self.buttons['a'].config(text=data['all_answers'][0], state= "enabled")
        self.buttons['b'].config(text=data['all_answers'][1], state= "enabled")
        self.buttons['c'].config(text=data['all_answers'][2], state= "enabled")
        self.buttons['d'].config(text=data['all_answers'][3], state= "enabled")
        
    def send_answer(self, answer):
        import clients
        self.buttons['a'].config(state= "disabled")
        self.buttons['b'].config(state= "disabled")
        self.buttons['c'].config(state= "disabled")
        self.buttons['d'].config(state= "disabled")

        player_answer = self.buttons[answer]['text']
        clients.getAnswer(player_answer)
    
    def recieve_players_score(self,score1,score2):
        import clients
        self.score_label.config(text=f"Youre score: {score1}")
        self.opponent_score_label.config(text=f"Opponents score: {score2}")
        clients.getNextQuestion()
        
       
               
               
               
       
       
               
    # def game_over(self):
    #     print("gameover")
    #     print(f"youre score is: {self.score}")
    #     exit()
        
    
  
    
    # def check_answer(self, answer):
    #     player_answer = self.buttons[answer]['text']
    #     if player_answer == self.all_questions[self.counter]['correct_answer']:
    #         self.correct_answer()
    #     else:
    #         self.wrong_answer()
        
    #     self.counter += 1
    #     self.next_question()

