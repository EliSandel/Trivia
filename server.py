import socket

client1_counter = 0
client2_counter = 0

def getQuestions():
    #getting question from api class
    
    return
    
def getAnswers():
    #getting the answers from api class
    
    return

def checkAnswers(client1_ans,client2_ans):
    #checking the correct answer and returns 1 or 2 according to the the correct client
    
    return

def checkToExit(check1,check2):
    if check1 == "exit" or check1 == "Exit" or check1 == "EXIT":
        return "close connection from client1"
    elif check2 == "exit" or check2 == "Exit" or check2 == "EXIT":
        return "close connection from client2"



def main():
    #open socket1
    server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket1.bind(("0.0.0.0",8822))
    server_socket1.listen()
    print("socket1 is up and ready!")
    (client_socket1,client_address1) = server_socket1.accept()
    print("client1 connected")
    
    #open socket2
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket2.bind(("0.0.0.0",8833))
    server_socket2.listen()
    print("socket2 is up and ready!")
    (client_socket2,client_address2) = server_socket2.accept()
    print("client2 connected")
    
    #the sockets will ryn until the while is closed
    while True:
        question = getQuestions()
        answers = getAnswers()
        
        #sending to clients the question
        client_socket1.send(str(question).encode())
        client_socket2.send(str(question).encode())
        
        #sending to clients the answers
        client_socket1.send(str(answers).encode())
        client_socket2.send(str(answers).encode())
        
        #getting the chossen answers from clients
        client1_ans = client_socket1.recv(1024)
        client2_ans = client_socket2.recv(1024)
        
        #checking who is coorect and updates the correct counter
        if checkAnswers(client1_ans,client2_ans) == 1:
            client1_counter = client1_counter + 1
        else:
            client2_counter = client2_counter + 1
            
        #sending the counters to the clients
        client_socket1.send("counters".encode() + str(client1_counter).encode() +str(client2_counter).encode())    
        client_socket2.send("counters".encode() + str(client1_counter).encode() +str(client2_counter).encode())    
        
        #checking if need to exit game
        check1 = client_socket1.recv(1024)
        check2 = client_socket2.recv(1024)
        check_to_exit = checkToExit(check1.decode(),check2.decode())
        if check_to_exit[16:] == "close connection":
            if check_to_exit[:7] == "client1":
                client_socket1.send("the game was closed by you:".encode())
                client_socket2.send("the game was closed by client1".encode())
            else:
                client_socket1.send("the game was closed by client2".encode())
                client_socket2.send("the game was closed by you:".encode())
        print("closing connections:")
        client_socket1.close()
        client_socket2.close()
        
        
        
    
    