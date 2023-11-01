import tkinter as tk
from functools import partial  # Import functools.partial


class GameGraphics:
    def __init__(self, root, all_questions):
        self.root = root
        self.all_questions = all_questions
        self.counter = 0
        self.score = 0
        
        self.gui_setup()
        
    def gui_setup(self):
        self.root.title("Trivia")
        self.root.config(padx=50, pady=50, bg="white")
        
        
        self.question_label = tk.Label(text="question")
        self.buttons = {}
        self.buttons['a'] = tk.Button(text="a", command=partial(self.check_answer, 'a'))
        self.buttons['b'] = tk.Button(text="b", command=partial(self.check_answer, 'b'))
        self.buttons['c'] = tk.Button(text="c", command=partial(self.check_answer, 'c'))
        self.buttons['d'] = tk.Button(text="d", command=partial(self.check_answer, 'd'))
        
        self.question_label.grid(row=0)
        self.buttons['a'].grid(row=1)
        self.buttons['b'].grid(row=2)
        self.buttons['c'].grid(row=3)
        self.buttons['d'].grid(row=4)
        
        self.next_question()


        
        
    
    def next_question(self):
        if self.counter == len(self.all_questions):
            self.game_over()
        else:
            current_question_data = self.all_questions[self.counter]
            self.question_label.config(text=current_question_data['question'])
            self.buttons['a'].config(text=current_question_data['all_answers'][0])
            self.buttons['b'].config(text=current_question_data['all_answers'][1])
            self.buttons['c'].config(text=current_question_data['all_answers'][2])
            self.buttons['d'].config(text=current_question_data['all_answers'][3])
            
            
    
    def game_over(self):
        print("gameover")
        print(f"youre score is: {self.score}")
        exit()
        
    
    
    def correct_answer(self):
        self.score += 1
        print("youre right")
    
    
    def wrong_answer(self):
        print("youre wrong")
    
    def check_answer(self, answer):
        player_answer = self.buttons[answer]['text']
        if player_answer == self.all_questions[self.counter]['correct_answer']:
            self.correct_answer()
        else:
            self.wrong_answer()
        
        self.counter += 1
        self.next_question()


# root = tk.Tk()
# data = [
#     {
#         'question': 'Which of these is NOT an Australian state or territory?', 
#         'correct_answer': 'Alberta', 
#         'incorrect_answers': ['New South Wales', 'Victoria', 'Queensland'], 
#         'all_answers': ['New South Wales', 'Victoria', 'Queensland', 'Alberta']
#     }, 
#     {
#         'question': 'Which of the following countries was not an axis power during World War II?', 
#         'correct_answer': ' Soviet Union', 
#         'incorrect_answers': ['Italy', 'Germany', 'Japan'], 
#         'all_answers': ['Italy', 'Germany', 'Japan', ' Soviet Union']
#     }
# ]

# gamegraphics = GameGraphics(root,data)
# root.mainloop()