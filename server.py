import socket
import question_data
import select

client1_counter = 0
client2_counter = 0
api_class = question_data.TriviaApi()  

server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket1.bind(("0.0.0.0",8822))
server_socket1.listen()
print("socket1 is up and ready!")
(client_socket1,client_address1) = server_socket1.accept()
print("first client connected")
(client_socket2,client_address2) = server_socket1.accept()
print("secound client connected")



def checkToExit(check1):
    if check1 == "exit" or check1 == "Exit" or check1 == "EXIT":
        return "close connection from client1"
    
    
    

# def sendQuestionsToClient():
#     global client_socket1,client_socket2
#     counter = 100
#     while counter > 0:
#         client_socket1.send("question".encode())
#         client_socket2.send("question".encode())
#         check = client_socket1.recv(1024).decode()
#         check2 = client_socket2.recv(1024).decode()
#         while check != "a" and check2 != "a":
#             check = client_socket1.recv(1024).decode()
#             check2 = client_socket2.recv(1024).decode()
        
    
def sendQuestion(question_and_ans):
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
        ###update th back class that they got the questions###
        
def waitForAnswer():
    ready1 = select.select([client_socket1], [], [], 0.1)
    ready2 = select.select([client_socket2], [], [], 0.1)
    while not ready1[0]:
        ready1 = select.select([client_socket1], [], [], 0.1)
    answer1 = client_socket1.recv(1024).decode()
    
    while not ready2[0]:
        ready2 = select.select([client_socket2], [], [], 0.1)
    answer2 = client_socket2.recv(1024).decode() 
    
def main():
   
    
        
    data = api_class.get_trivia_questions(amount=2)
    #the sockets will ryn until the while is closed
    while True:
         #checking if need to exit game
        # check1 = client_socket1.recv(1024)
        # check2 = client_socket2.recv(1024)
        # check_to_exit = checkToExit(check1.decode())
        # if check_to_exit[:16] == "close connection":
        #     if check_to_exit[-7:] == "client1":
        #         client_socket1.send("closing: the game was closed by you:".encode())
        #         # client_socket2.send("closing: the game was closed by client1".encode())
        #         break
        #     else:
        #         client_socket1.send("closing: the game was closed by client2".encode())
        #         # client_socket2.send("closing: the game was closed by you:".encode())
        #         break
        # else:
        
        # client_socket2.send("data".encode() + str(data).encode())
        
        #getting the chossen score from clients
        client1_score = client_socket1.recv(1024).decode()
        # client2_score = client_socket2.recv(1024).decode()
        
        print(client1_score + "gfcvgbhnjkhgfd")
        client1_counter = int(client1_score)
        # client2_counter = int(client2_score)
            
        #sending the counters to the clients
        client_socket1.send("counters".encode() + "client1 counter".encode() + str(client1_counter).encode() + "client2 counter".encode() + str(client2_counter).encode())    
        # client_socket2.send("counters".encode() + "client1 counter".encode() + str(client1_counter).encode() + "client2 counter".encode() + str(client2_counter).encode())    
        
        
    print("closing connections:")    
    client_socket1.close()
    # client_socket2.close()
    
# sendQuestionsToClient()
            
        
        
    
    