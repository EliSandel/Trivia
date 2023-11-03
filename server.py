import socket
import question_data
import select
import backend

client1_counter = 0
client2_counter = 0
backend = backend.Backend()
api_class = question_data.TriviaApi()  

server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket1.bind(("0.0.0.0",8822))
server_socket1.listen()
print("socket1 is up and ready!")
(client_socket1,client_address1) = server_socket1.accept()
print("first client connected")
(client_socket2,client_address2) = server_socket1.accept()
print("secound client connected")



# def checkToExit(check1):
#     if check1 == "exit" or check1 == "Exit" or check1 == "EXIT":
#         return "close connection from client1"
    
        
def reciveTheFullServer_sent(x,server_sent):
    server_sent = server_sent[x:]
    return server_sent


    
def sendQuestion():
    question_and_ans = backend.next_question()
    #sending to clients the question
    client_socket1.send("question".encode() + str(question_and_ans).encode())
    client_socket2.send("question".encode() + str(question_and_ans).encode())
    check1 = client_socket1.recv(1024).decode() 
    check2 = client_socket1.recv(1024).decode() 
    while check1 == "didnt got question":
        client_socket1.send("question".encode() + str(question_and_ans).encode())
    while check2 == "didnt got question":
        client_socket2.send("question".encode() + str(question_and_ans).encode())
    if check1 == "got question" and check2 == "got question":
        ###you can update th back class that they got the questions### 
        return
        
        
def waitForAnswers():
    ready1 = select.select([client_socket1], [], [], 0.1)
    ready2 = select.select([client_socket2], [], [], 0.1)
    while not ready1[0]:
        ready1 = select.select([client_socket1], [], [], 0.1)
    answer1 = client_socket1.recv(1024).decode()
    if answer1[:15] != "selected answer":
        print("got uncorrect messege from client1")
    else:
        answer1 = reciveTheFullServer_sent(15,answer1)
        client_socket1.send("got your answer".encode())
    
    while not ready2[0]:
        ready2 = select.select([client_socket2], [], [], 0.1)
    answer2 = client_socket2.recv(1024).decode() 
    if answer2[:15] != "selected answer":
        print("got uncorrect messege from client1")
    else:
        answer2 = reciveTheFullServer_sent(15,answer2)
        client_socket2.send("got your answer".encode())
        
        backend.check_answer(0,answer1)
        backend.check_answer(1,answer2)        
        infoForClients()
                         
def infoForClients():
    player1_score = backend.get_score(0)
    player2_score = backend.get_score(1)
    client_socket1.send("info".encode() + "a".encode() + str(player1_score).encode() + "b".encode() + str(player2_score).encode())
    client_socket2.send("info".encode() + "a".encode() + str(player2_score).encode() + "b".encode() + str(player1_score).encode())
    
    ready1 = select.select([client_socket1], [], [], 0.1)
    ready2 = select.select([client_socket2], [], [], 0.1)
    while not ready1[0]:
        ready1 = select.select([client_socket1], [], [], 0.1)
    answer1 = client_socket1.recv(1024).decode()
    if answer1[:13] != "next question":
        print("got unccorect messege from client1")
    else:
        while not ready2[0]:
            ready2 = select.select([client_socket2], [], [], 0.1)
        answer2 = client_socket2.recv(1024).decode()
        if answer2[:13] != "next question":
            print("got unccorect messege")
        else:
            sendQuestion()        

   
sendQuestion()
        
        
