import graphics
import tkinter as tk

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

gamegraphics = graphics.GameGraphics(root)
gamegraphics.next_question(data[0])
root.mainloop()