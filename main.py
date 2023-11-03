import a
import tkinter as tk

root = tk.Tk()
data = [
    {
        'question': 'Which of these is "NOT" an Australian state or territory?', 
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

gamegraphics = a.GameGraphics(root)
gamegraphics.next_question(str({'question': "What does the letter 'S' stand for in 'NASA'?", 'correct_answer': 'Space', 'incorrect_answers': ['Science', 'Society', 'Star'], 'all_answers': ['Science', 'Society', 'Star','Space']}))
root.mainloop()