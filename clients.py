import socket
import graphics
import tkinter as tk

root = tk.Tk()
my_counter = 0
rival_counter = 0
#open socket with server
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1",8822))
print("connected")




def updateCounters(server_sent):
    global my_counter
    global rival_counter
    find_counter2_start = server_sent.find("client2 counter")
    my_counter = int(server_sent[23:find_counter2_start])
    rival_counter = int(server_sent[find_counter2_start + 15:])
    
def reciveTheFullServer_sent(x,server_sent):
    server_sent = server_sent[x:]
    return server_sent
    
    
def close_comuunication():
        global exit
        exit = True
def getAnswer(answer):
    
    return


def main():
    while True:
            server_sent = my_socket.recv(1024).decode()
            while server_sent[:8] != "question": 
                my_socket.send("didnt got question")
                server_sent = my_socket.recv(1024).decode()
            my_socket.send("got question".encode())
            
            #checking what the server sent
            if server_sent[:8] == "question":
                server_sent = reciveTheFullServer_sent(8,server_sent)
            else:
                print("404 not found")
            # my_socket.send(str(game_graphics.score).encode())
                
            server_sent = my_socket.recv(1024).decode()
            if server_sent[:8] == "counters":
                updateCounters(server_sent)
            else:
                print("404 not found counter")
    
    print("client1 closed")
    my_socket.close()    
    
# counter = 0   
# def trys():
#     global counter,my_socket
#     counter1 = 100
#     while counter1 > 0:
#         server = my_socket.recv(1024).decode()
#         counter = counter + 1
#         print(str(counter) + server)
#         my_socket.send("a".encode())
#         counter1 = counter1 -1

    
# trys()