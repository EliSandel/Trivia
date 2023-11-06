import socket
import graphics
import tkinter as tk
import select
import threading

class Clients():
    
    
    def __init__(self):
        self.my_socket_room = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.root = tk.Tk()
        self.gamegraphics = graphics.GameGraphics(self.root, self)
        

    def openClient(self):
        self.my_socket_room.connect(("127.0.0.1",8833))
        print("connected to rooms server")
        his_mind = input("options: create room/join room?")
        get_username = input("whats your name?")
        if his_mind == "join room":
            get_num_of_room = input("whats the number of room?")
            self.my_socket_room.send(his_mind.encode() + "N".encode() +  str(get_username).encode() + "R".encode() + str(get_num_of_room).encode())
            rooms_answer = self.my_socket_room.recv(1024).decode()
        else:
            self.my_socket_room.send(his_mind.encode() + "N".encode() +  str(get_username).encode())
            rooms_answer = self.my_socket_room.recv(1024).decode()
            if rooms_answer[:28] == "room was created succesfully":
                find_N = rooms_answer.find("N")
                my_room_number = rooms_answer[find_N+1:]
                startGame = input("press enter to start geme")
                self.my_socket_room.send("start game".encode() + "R".encode() + my_room_number.encode())
        
        
        
        
        if rooms_answer[:28] == "room was created succesfully" or rooms_answer == "joined succesfully":
            print(rooms_answer)
            rooms_answer = self.my_socket_room.recv(1024).decode()
            print(rooms_answer)
            rooms_answer = self.my_socket_room.recv(1024).decode()
            print(rooms_answer)
    
    
            #open socket with server
        # self.my_socket.connect(("127.0.0.1",8833))
        # print("connected")


    def reciveTheFullServer_sent(self,x,server_sent):            
        server_sent = server_sent[x:]
        return server_sent
        
        
  
            
    def sendInfoToGraphics(self,server_sent):
        print("got info")
        server_sent = self.reciveTheFullServer_sent(4,server_sent)
        find_o = server_sent.find("o")
        my_score = server_sent[1:find_o]
        others_score = server_sent[find_o + 1:]
        print("got answer")
        self.gamegraphics.recieve_players_score(my_score,others_score) 
        
        
    def getAnswer(self,answer):
        print("send answer")
        self.my_socket_room.send("selected answer".encode()+str(answer).encode())
        
                
                
    def getNextQuestion(self):
        self.my_socket_room.send("next question".encode())
        self.main()

    def runGui(self):
        self.root.mainloop()
        pass
        
    def gettingQuestions(self,server_sent):
        server_sent = self.reciveTheFullServer_sent(8,server_sent)
        print("sending queestoin to graphics")
        self.gamegraphics.next_question(server_sent)
        
    def main(self):
        while True:
            print("waiting for recive")
            server_sent = self.my_socket_room.recv(1024).decode()
            if server_sent[:8] == "question":
                self.gettingQuestions(server_sent)
            elif server_sent[:4] == "info":
                self.sendInfoToGraphics(server_sent)

           
        
        
    
        
    def startGmae(self):
        self.openClient()
        thread2 = threading.Thread(target=self.main)
        thread2.start()
        self.runGui()
        
        
            
if __name__ == '__main__':
    clients = Clients()
    clients.startGmae()
    clients.openClient()
    



