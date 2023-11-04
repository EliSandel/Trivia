import socket
import graphics
import tkinter as tk
import select
import threading

class Clients():
    
    
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.root = tk.Tk()
        self.gamegraphics = graphics.GameGraphics(self.root)
        

    def openClient(self):
        #open socket with server
        self.my_socket.connect(("127.0.0.1",8822))
        print("connected")


    def reciveTheFullServer_sent(self,x,server_sent):            
        server_sent = server_sent[x:]
        return server_sent
        
        
    # def close_comuunication():
    #         global exit
    #         exit = True
            
            
    def getAnswer(self,answer):
        self.my_socket.send("selected answer".encode()+str(answer).encode())
        check = self.my_socket.recv(1024).decode()
        if check == "got your answer":
            print("my answer was sent succesfull! waiting for info")
            ready = select.select([self.my_socket], [], [], 0.1)
            while not ready[0]:
                ready = select.select([self.my_socket], [], [], 0.1)
            server_sent = self.my_socket.recv(1024).decode()
            if server_sent[:4] == "info":
                server_sent = self.reciveTheFullServer_sent(4,server_sent)
                find_b = server_sent.find("b")
                player1_score = server_sent[2:find_b]
                player2_score = server_sent[find_b + 1:]
                self.gamegraphics.recieve_players_score(player1_score,player2_score)  
                
            else:
                print("got uncorrect answer")
                
    def getNextQuestion(self):
        self.my_socket.send("next question".encode())
        self.main()

    def runGui(self):
        self.root.mainloop()
        

    def main(self):
        while True:
                ready = select.select([self.my_socket], [], [], 0.1)
                while not ready[0]:
                    ready = select.select([self.my_socket], [], [], 0.1)
                    print("still waiting")
                server_sent = self.my_socket.recv(1024).decode()
                print("stop waiting")

                while server_sent[:8] != "question": 
                    self.my_socket.send("didnt got question")
                    server_sent = self.my_socket.recv(1024).decode()
                self.my_socket.send("got question".encode())
                server_sent = self.reciveTheFullServer_sent(8,server_sent)
                print(server_sent)
                self.gamegraphics.next_question(server_sent)
        
        print("client1 closed")
        self.my_socket.close()  
        
    def startGmae(self):
        self.openClient()
        thread1 = threading.Thread(target=self.runGui)
        thread2 = threading.Thread(target=self.main)
        # thread1.start()
        thread2.start()
        self.runGui()
            
if __name__ == '__main__':
    clients = Clients()
    clients.startGmae()

    



