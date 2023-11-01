import socket

my_counter = 0
rival_counter = 0

def theAnswers():
    
    return



def updateCounters(server_sent):
    global my_counter
    global rival_counter
    find_counter2_start = server_sent.find("client2 counter")
    my_counter = int(server_sent[23:find_counter2_start])
    rival_counter = int(server_sent[find_counter2_start + 15:])
    
def close_comuunication():
        global exit
        exit = True

def main():
    #open socket with server
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1",8822))
    
    while True:
         if exit == True:
            my_socket.send("exit".encode())
            break
         else:
            server_sent = my_socket.recv(1024).decode()
            
            #checking what the server sent
            if server_sent[:4] == "data":
              ##########theQuestions(server_sent)#######################
            else:
                print("404 not found")
                
           ###### my_socket.send(client1.sendscore.encode())############
                
            server_sent = my_socket.recv(1024).decode()
            if server_sent[:8] == "counters":
                updateCounters(server_sent)
            else:
                print("404 not found counter")
    
    print("client1 closed")
    my_socket.close()    