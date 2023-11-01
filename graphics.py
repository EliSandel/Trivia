import tkinter as tk

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
        self.answer_a_button = tk.Button(text="a", command=self.check_answer)
        self.answer_b_button = tk.Button(text="b", command=self.check_answer)
        self.answer_c_button = tk.Button(text="c", command=self.check_answer)
        self.answer_d_button = tk.Button(text="d", command=self.check_answer)
        
        self.question_label.grid(row=0)
        self.answer_a_button.grid(row=1)
        self.answer_b_button.grid(row=2)
        self.answer_c_button.grid(row=3)
        self.answer_d_button.grid(row=4)
        
        self.next_question()


        
        
    
    def next_question(self):
        if self.counter == len(self.all_questions):
            self.game_over()
        else:
            current_question_data = self.all_questions[self.counter]
            self.question_label.config(text=current_question_data['question'])
            self.answer_a_button.config(text=current_question_data['all_answers'][0])
            self.answer_b_button.config(text=current_question_data['all_answers'][1])
            self.answer_c_button.config(text=current_question_data['all_answers'][2])
            self.answer_d_button.config(text=current_question_data['all_answers'][3])
        
    
    def game_over(self):
        pass
    
    
    def correct_answer(self):
        pass
    
    
    def wrong_answer(self):
        pass
    
    def check_answer(self):
        
        
        self.next_question()


root = tk.Tk()
data = [
    {
        'question': 'Which of these is NOT an Australian state or territory?', 
        'correct_answer': 'Alberta', 
        'incorrect_answers': ['New South Wales', 'Victoria', 'Queensland'], 
        'all_answers': ['New South Wales', 'Victoria', 'Queensland', 'Alberta']
    }, 
    {
        'question': 'Which of the following countries was not an axis power during World War II?', 
        'correct_answer': ' Soviet Union', 
        'incorrect_answers': ['Italy', 'Germany', 'Japan'], 
        'all_answers': ['Italy', 'Germany', 'Japan', ' Soviet Union']
    }
]

gamegraphics = GameGraphics(root,data)
root.mainloop()