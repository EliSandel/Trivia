import socket
import graphics
import tkinter as tk
import select
import threading


root = tk.Tk()
gamegraphics = graphics.GameGraphics(root)



#open socket with server
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1",8822))
print("connected")


def reciveTheFullServer_sent(x,server_sent):
    server_sent = server_sent[x:]
    return server_sent
    
    
# def close_comuunication():
#         global exit
#         exit = True
        
        
def getAnswer(answer):
    my_socket.send("selected answer".encode()+str(answer).encode())
    check = my_socket.recv(1024).decode()
    if check == "got your answer":
        print("my answer was sent succesfull! waiting for info")
        ready = select.select([my_socket], [], [], 0.1)
        while not ready[0]:
            ready = select.select([my_socket], [], [], 0.1)
        server_sent = my_socket.recv(1024).decode()
        if server_sent[:4] == "info":
            server_sent = reciveTheFullServer_sent(4,server_sent)
            find_b = server_sent.find("b")
            player1_score = server_sent[2:find_b]
            player2_score = server_sent[find_b + 1:]
            gamegraphics.recieve_players_score(player1_score,player2_score)  
            
        else:
            print("got uncorrect answer")
            
def getNextQuestion():
    my_socket.send("next question".encode())
    main()

def runGui():
    root.mainloop()
    

def main():
    while True:
            ready = select.select([my_socket], [], [], 0.1)
            while not ready[0]:
                ready = select.select([my_socket], [], [], 0.1)
                print("still waiting")
            server_sent = my_socket.recv(1024).decode()
            print("stop waiting")

            while server_sent[:8] != "question": 
                my_socket.send("didnt got question")
                server_sent = my_socket.recv(1024).decode()
            my_socket.send("got question".encode())
            server_sent = reciveTheFullServer_sent(8,server_sent)
            gamegraphics.next_question(server_sent)
    
    print("client1 closed")
    my_socket.close()    
    
thread1 = threading.Thread(target=runGui)
thread2 = threading.Thread(target=main)
thread1.start()
thread2.start()


