import server
import socket
import threading
import backend

class Rooms():
    def __init__(self):
        self.room_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.room_socket.bind(("0.0.0.0",8833))
        self.room_socket.listen()
        print("room socket is ready!")
        self.roomsNames = []
        # self.roomsSockets = []
        self.rooms = []
        self.room_num = 0
        self.backend = backend.Backend()



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
                find_R = client_request.find("R")
                room_id = client_request[find_R +1:]
                print("room " + str(room_id) + " have been start game!")
                self.startingGame(client_request)  
            
                 
                
    def startingGame(self,client_request):
        find_R = client_request.find("R")
        room_id = client_request[find_R +1:]
        for index in self.rooms:
            if index['id'] == room_id:
                the_list_of_sockets = self.rooms[index['sockets']]
                the_list_of_names = self.rooms[index['playe_names']]
        # the_list_of_sockets = self.roomsSockets[int(number_of_room)]
        # the_list_of_names = self.roomsNames[int(number_of_room)]
        # for x in the_list_of_sockets:
        #         client_room = x
        #         client_room.send("pass to server class".encode())
        serverGame = server.Server(the_list_of_sockets,the_list_of_names)
                
        
        
        
    def joinRoom(self,client_request,client_room,find_N):
        find_R = client_request.find("R")
        room_id = client_request[find_R+1:]
        player_name = client_request[find_N + 1:find_R]
        # self.roomsNames[int(room_id)].append(player_name)
        # self.roomsSockets[int(room_id)].append(client_room)
        check = False
        for index in self.rooms:
            if index['id'] == room_id:
                index['player_names'].append(player_name)
                index['sockets'].append(client_room)
                room_name = index['room_name']
                host_name = index['host_name']
                client_room.send("joined succesfully".encode() + "R".encode() + room_name.encode() + "H".encode() + host_name.encode())
                check = True
                print("joined room")
                break
        if check == False:
              client_room.send("failed to join not found room id".encode() + "I".encode() + room_id.encode())
              print("rejected to join")
                

    def createRoom(self,client_request,client_room,find_N):
        room_id = self.backend.generate_random_room_id()#######################
        find_R = client_request.find("R")
        host_name = client_request[find_N + 1:find_R]
        room_name = client_request[find_R + 1:]
        # self.roomsNames.append([username])
        # self.roomsSockets.append([client_room])
        self.rooms.append(
            {
              "id": room_id,
              "host_name":host_name,
              "room_name": room_name,
              "player_names": [],
              "sockets" :[client_room]
            }
        )
        
        client_room.send("room was created succesfully".encode() + "I".encode() + str(room_id).encode())
        self.room_num += 1
        print("room created!")
        print("there are " +str(self.room_num)+ " rooms")
        

    
        
if __name__ == '__main__':
   rooms = Rooms()
   rooms.main()