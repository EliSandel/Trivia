import tkinter as tk
from functools import partial 
import test
import ast
import threading

class GameGraphics:
    def __init__(self, root, client):
        self.root = root
        self.counter = 0
        self.score = 0
        self.client = client
        self.gui_setup()
        
    def gui_setup(self):
        self.root.title("Trivia")
        self.root.config(padx=50, pady=50, bg="white")
        
        self.score_label = tk.Label(text=f"score: {0}")
        self.opponent_score_label = tk.Label(text=f"opponent score: {0}")
        self.question_label = tk.Label(text="question")
        self.waiting_label = tk.Label(text="Waiting for opponent's answer", fg="red")  # Add a label for waiting message
        self.buttons = {}
        self.buttons['a'] = tk.Button(text="a", command=partial(self.start_thread, 'a'))
        self.buttons['b'] = tk.Button(text="b", command=partial(self.start_thread, 'b'))
        self.buttons['c'] = tk.Button(text="c", command=partial(self.start_thread, 'c'))
        self.buttons['d'] = tk.Button(text="d", command=partial(self.start_thread, 'd'))
        
        self.score_label.grid(row=0, column=0)
        self.opponent_score_label.grid(row=0, column=2)
        self.question_label.grid(row=1, column=1)
        self.buttons['a'].grid(row=2, column=1)
        self.buttons['b'].grid(row=3, column=1)
        self.buttons['c'].grid(row=4, column=1)
        self.buttons['d'].grid(row=5, column=1)
        


        
    def next_question(self, data):
        data = ast.literal_eval(data)
        self.question_label.config(text=data['question'])
        self.buttons['a'].config(text=data['all_answers'][0], state= "normal")
        self.buttons['b'].config(text=data['all_answers'][1], state= "normal")
        self.buttons['c'].config(text=data['all_answers'][2], state= "normal")
        self.buttons['d'].config(text=data['all_answers'][3], state= "normal")
        
    def send_answer(self, answer):
        self.buttons['a'].config(state= "disabled")
        self.buttons['b'].config(state= "disabled")
        self.buttons['c'].config(state= "disabled")
        self.buttons['d'].config(state= "disabled")

        self.waiting_label.grid(row=6, column=1)
        player_answer = self.buttons[answer]['text']
        self.client.getAnswer(player_answer)
    
    def recieve_players_score(self,score1,score2):
        self.waiting_label.grid_forget()
        self.score_label.config(text=f"Youre score: {score1}")
        self.opponent_score_label.config(text=f"Opponents score: {score2}")
        self.client.getNextQuestion()
        
    def start_thread(self, answer): #when clicking the button i want to call the button func from within a thread so it wont crash
        threading.Thread(target= self.send_answer, args=(answer)).start()
        
              
    def game_over(self, winners):
        self.root.destroy()
        root = tk.Tk()
        if len(winners) == 1:
            winner_label = tk.Label(text=f"Player {winners[0]} won the game!")
            winner_label.pack()
        else:
            title_label = tk.Label(text=f"The winners are")
            title_label.pack()
            for winner in winners:
                winner_label = tk.Label(text=f"Player {winner}!")
                winner_label.pack()
        
        root.protocol("WM_DELETE_WINDOW", root.quit) #close the program when the window is closed
        

