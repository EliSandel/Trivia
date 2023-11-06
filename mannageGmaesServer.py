import server
import socket
import threading

class Rooms():
    def __init__(self):
        self.room_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.room_socket.bind(("0.0.0.0",8833))
        self.room_socket.listen()
        print("room socket is ready!")
        self.roomsID = []
        self.roomsSockets = []
        self.room_num = 0



    def main(self):
        while True:
            (client_room,client_address) = self.room_socket.accept() 
            client_request = client_room.recv(1024).decode()
            find_N = client_request.find("N")
            his_mind = client_request[:find_N]
            
            if his_mind == "create room":
               threading.Thread(target=self.checkForStartingGmae,args=(client_room,)).start()
               self.createRoom(client_request,client_room,find_N)
                
            elif his_mind == "join room":
                self.joinRoom(client_request,client_room,find_N)
                
            
                
                
    def checkForStartingGmae(self,client_room):
        while True:
            client_request = client_room.recv(1024).decode()
            if client_request[:10] == "start game":
                self.startingGame(client_request)  
            
                 
                
    def startingGame(self,client_request):
        find_R = client_request.find("R")
        number_of_room = client_request[find_R +1:]
        the_list_of_sockets = self.roomsSockets[int(number_of_room)]
        the_list_of_names = self.roomsID[int(number_of_room)]
        for x in the_list_of_sockets:
                client_room = x
                client_room.send("pass to server class".encode())
        serverGame = server.Server(the_list_of_sockets,the_list_of_names)
                
        
        
        
    def joinRoom(self,client_request,client_room,find_N):
        find_R = client_request.find("R")
        room_number = client_request[find_R+1:]
        username = client_request[find_N + 1:find_R]
        self.roomsID[int(room_number)].append(username)
        self.roomsSockets[int(room_number)].append(client_room)
        client_room.send("joined succesfully".encode())
        print("joined room")
                
                

    def createRoom(self,client_request,client_room,find_N):
        username = client_request[find_N + 1:]
        self.roomsID.append([username])
        self.roomsSockets.append([client_room])
        client_room.send("room was created succesfully".encode() + "N".encode() + str(self.room_num).encode())
        self.room_num += 1
        print("room created!")
        

    
        
if __name__ == '__main__':
   rooms = Rooms()
   rooms.main()