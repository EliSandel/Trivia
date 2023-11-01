import socket
import question_data

client1_counter = 0
client2_counter = 0
api_class = question_data.TriviaApi()  




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
    
    open socket2
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket2.bind(("0.0.0.0",8833))
    server_socket2.listen()
    print("socket2 is up and ready!")
    (client_socket2,client_address2) = server_socket2.accept()
    print("client2 connected")
    
    data = api_class.get_trivia_questions(amount=2)
    #the sockets will ryn until the while is closed
    while True:
         #checking if need to exit game
        check1 = client_socket1.recv(1024)
        check2 = client_socket2.recv(1024)
        check_to_exit = checkToExit(check1.decode(),check2.decode())
        if check_to_exit[:16] == "close connection":
            if check_to_exit[-7:] == "client1":
                client_socket1.send("closing: the game was closed by you:".encode())
                client_socket2.send("closing: the game was closed by client1".encode())
                break
            else:
                client_socket1.send("closing: the game was closed by client2".encode())
                client_socket2.send("closing: the game was closed by you:".encode())
                break
        else:
            #sending to clients the question
            client_socket1.send("data".encode() + str(data).encode())
            client_socket2.send("data".encode() + str(data).encode())
            
            #getting the chossen score from clients
            client1_score = client_socket1.recv(1024).decode()
            client2_score = client_socket2.recv(1024).decode()
            
            print(client1_score + "gfcvgbhnjkhgfd")
            client1_counter = int(client1_score)
            client2_counter = int(client2_score)
                
            #sending the counters to the clients
            client_socket1.send("counters".encode() + "client1 counter".encode() + str(client1_counter).encode() + "client2 counter".encode() + str(client2_counter).encode())    
            client_socket2.send("counters".encode() + "client1 counter".encode() + str(client1_counter).encode() + "client2 counter".encode() + str(client2_counter).encode())    
            
        
    print("closing connections:")    
    client_socket1.close()
    client_socket2.close()
    
main()
            
        
        
    
    