import re
import tkinter as tk
from functools import partial 
import ast
import threading
import random
from tkinter import messagebox

class GameGraphics:
    def __init__(self, root, client):
        self.root = root
        self.all_scores = []
        self.all_names = []
        self.client = client
        self.my_name = ""
        self.room_name = ""
        self.landing_page_gui_setup()
        
    def main_game_gui_setup(self, array_of_names):
        self.all_names = eval(array_of_names)
        self.clear_screen()
        self.root.title("Trivia")
        self.root.config(padx=50, pady=50, bg="white")
        
        self.score_label = tk.Label(text=f"score: {0}")
        self.question_label = tk.Label(text="question")
        self.waiting_label = tk.Label(text="Waiting for opponent's answer", fg="red")  # Add a label for waiting message
        self.buttons = {}
        self.buttons['a'] = tk.Button(text="a", command=partial(self.start_thread, 'a'))
        self.buttons['b'] = tk.Button(text="b", command=partial(self.start_thread, 'b'))
        self.buttons['c'] = tk.Button(text="c", command=partial(self.start_thread, 'c'))
        self.buttons['d'] = tk.Button(text="d", command=partial(self.start_thread, 'd'))
        
        self.score_label.grid(row=0, column=1)
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
    
    def recieve_players_score(self,my_score, all_scores): #str myscore, str list of all scores
        self.all_scores = eval(all_scores)
        self.waiting_label.grid_forget()
        self.score_label.config(text=f"Youre score: {my_score}")
        #call the window for showing the scoreedborad and then scoreboard should call nextquestion
        self.client.getNextQuestion()
        
    def start_thread(self, answer): #when clicking the button i want to call the button func from within a thread so it wont crash
        threading.Thread(target= self.send_answer, args=(answer)).start()
        
              
    def game_over(self, all_scores, all_indexes_of_high_score):#tell yehuda to add all_indexes
        self.all_scores = eval(all_scores)
        all_indexes_of_high_score = eval(all_indexes_of_high_score)
        self.clear_screen()
        
        if len(all_indexes_of_high_score) == 1:# to check if there are multiple winners or just one
            winner_message_label = tk.Label(text="The winner of the Trivia game is...").pack()
        else:
            winner_message_label = tk.Label(text=f"The {len(all_indexes_of_high_score)} winners of the Trivia game are...").pack()
        tk.Frame(height=20).pack#create empty space between the message
        
        #to find the winners
        for index in all_indexes_of_high_score:
            winner_name_score_label = tk.Label(text=f"{self.all_names[index]}: {self.all_scores[index]}").pack()
        
        #to print the rest of the players besides the winners and their scores
        all_players_label = tk.Label(text="All the rest of the players")
        for index,name in enumerate(self.all_names):
            if not index in all_indexes_of_high_score:
                name_score_label = tk.Label(text=f"{name}: {self.all_scores[index]}").pack()
    
    #all this is for the windows before the actual game
    def landing_page_gui_setup(self):# gui for landing page
        self.root.title("Welcome")
        self.root.geometry('300x300')
        
        self.name_label = tk.Label(text="Enter your name:").pack()
        self.name_entry = tk.Entry()
        self.name_entry.pack()
        
        self.host_button = tk.Button(text="Host game", command=self.host_game).pack()
        self.join_button = tk.Button(text="Join game", command=self.join_game).pack()
        
    def host_game(self):# called when user clicks host. saves users name, calls next window
        self.my_name = self.name_entry.get()
        if self.my_name:
            self.clear_screen()
            self.create_room_window() #call the next window
            
    def join_game(self):# when user clicks join first time. saves users name, calls next window
        self.my_name = self.name_entry.get()
        if self.my_name:
            self.clear_screen()
            self.join_room_window()
            
    def create_room_window(self):#called automatically after user clicks host. this is the window with the entry for room name
        self.clear_screen()
        room_name_label = tk.Label(text="Enter room name").pack()
        self.room_name_entry = tk.Entry()
        self.room_name_entry.pack()
        room_name_button = tk.Button(text="Create", command=self.send_room_name).pack()
    
    def send_room_name(self):# called when host enters room name and clicks create room.
        if self.room_name_entry.get():
            self.room_name = self.room_name_entry.get()
            self.clear_screen()
            #call function in client and pass room name
            self.client.create_room(self.my_name, self.room_name)
            #client should call host_start_game_window and pass room id. this is temporary
            
    def join_room_window(self):#is called automatically when user click join first time
        self.clear_screen()
        enter_id_label = tk.Label(text="Enter the ID of the room you want to join.\nYou must get the room ID from the host.")
        enter_id_label.pack()
        self.enter_id_entry = tk.Entry()
        self.enter_id_entry.pack()
        join_room_button = tk.Button(text="Join room", command=self.join_room)
        join_room_button.pack()
        self.join_room_button = join_room_button
        
    def join_room(self):#called when joiner clicks join room second time
        id = self.enter_id_entry.get()
        if id:
            # if not self.contains_non_digits(id):
            #     self.client.join_room(self.my_name, id)
            if self.contains_non_digits(id):
                # Show an error message to the user
                messagebox.showerror(title="Error", message=f"Room ID that you entered {id} is invalid.\nRoom ID consists of digits only.\nPlease try again.")
            else:
                # Attempt to join the room
                self.client.join_room(self.my_name, id)
    
    def contains_non_digits(self, id):
        for char in id:
            if not char.isdigit():
                return True
        return False
        
    def host_start_game_window(self, id):#this window is called by client. this is the window that the host can start the game from
        self.clear_screen()
        self.root.title("Trivia")
        room_name_label = tk.Label(text=f"Room name: {self.room_name}").pack()
        room_id_label = tk.Label(text=f"Room ID: {id}\nSend this ID to your friends that want to play with you.\nVerify that everyone joined the room before starting the game.").pack()
        start_game_button = tk.Button(text="Start Game",command= partial(self.client.start_game, id)).pack()
    
    def waiting_for_host_window(self, room_name, host_name):#this window is called by client after user puts in the room id
        self.clear_screen()
        success_message_label = tk.Label(text=f"You have successfully joined {room_name}.").pack()
        waiting_message_label = tk.Label(text=f"Waiting for {host_name} to start the game.").pack()
        
    def room_not_found(self, wrong_room_id):
        messagebox.showinfo(title="Error", message=f"Room ID that you entered {wrong_room_id} does not exist.\nPlease try again.")
        self.join_room_window()
        self.join_room_button.config(state=tk.NORMAL)
    
    def clear_screen(self):# removes all widgets from screen
        for widget in self.root.winfo_children():
            widget.destroy()
    
    
        


