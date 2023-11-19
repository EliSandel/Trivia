import array
import time
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
        # self.roomsNames = []
        # self.roomsSockets = []
        self.rooms = []
        self.room_ids = []
        self.room_num = 0
        self.backend = backend.Backend(self)
        self.thread = threading.Thread()


    def main(self):
        while True:
            (client_room,client_address) = self.room_socket.accept() 
            self.thread = threading.Thread(target=self.recv_every_client_in_thread,args=(client_room,))  #########################################################################################################################################
            self.thread.start()
            # print("wqaiting for rec")
            # client_request = client_room.recv(1024).decode()
            # find_N = client_request.find("N")
            # his_mind = client_request[:find_N]
            
            # if his_mind == "create room":
            #    threading.Thread(target=self.checkForStartingGmae,args=(client_room,)).start()
            #    self.createRoom(client_request,client_room,find_N)
                
            # elif his_mind == "join room":
            #     self.joinRoom(client_request,client_room,find_N)
                
    def recv_every_client_in_thread(self,client_room):
        flag = False
        while True:  
            print(flag)
            if flag == True:
                print("exittttttt")
                break
            else:
                print("wqaiting for rec")
                client_request = client_room.recv(1024).decode()
                find_N = client_request.find("N")
                his_mind = client_request[:find_N]
                
                if his_mind == "create room":
                    self.thread = threading.Thread(target=self.checkForStartingGmae,args=(client_room,))
                    self.thread.start()
                    flag = self.createRoom(client_request,client_room,find_N)
                    print(flag)
                    
                elif his_mind == "join room":
                    flag = self.joinRoom(client_request,client_room,find_N)
                    print(flag)
                    
            
                
                
    def checkForStartingGmae(self,client_room):
                client_request = client_room.recv(1024).decode()
                if client_request[:10] == "start game":
                    find_R = client_request.find("R")
                    room_id = client_request[find_R +1:]
                    print("room " + str(room_id) + " have been start game!")
                    self.startingGame(client_request)  
    
    
    def delete_room(self,room_id):
        for num_of_index,index in enumerate(self.rooms):
            if index["id"] == int(room_id):
                self.rooms.remove(num_of_index)
                print(f"{str(room_id)} room deleted")
        for num_of_index,index in enumerate(self.room_ids):
            if int(index) == int(room_id):
                self.room_ids.remove(num_of_index)
                print("id is deleted")
             
                 
                
    def startingGame(self,client_request):
        find_R = client_request.find("R")
        room_id = client_request[find_R +1:]
        for index in self.rooms:
            if index['id'] == int(room_id):
                the_list_of_sockets = index['sockets']
                the_list_of_names = index['player_names']
                for room in self.rooms:
                    if room['id'] == int(room_id):
                        for socket in room['sockets']:
                            socket.send("start game".encode() + str(the_list_of_names).encode())
                serverGame = server.Server(the_list_of_sockets,the_list_of_names,room_id)
                print("deleteds")   
                self.delete_room(room_id)             
                
        # the_list_of_sockets = self.roomsSockets[int(number_of_room)]
        # the_list_of_names = self.roomsNames[int(number_of_room)]
        # for x in the_list_of_sockets:
        #         client_room = x
        #         client_room.send("pass to server class".encode())
                
        
        
        
    def joinRoom(self,client_request,client_room,find_N):
        find_R = client_request.find("R")
        room_id = client_request[find_R+1:]
        room_id = int(room_id)
        print(room_id)
        player_name = client_request[find_N + 1:find_R]
        # self.roomsNames[int(room_id)].append(player_name)
        # self.roomsSockets[int(room_id)].append(client_room)
        check = False
        for index in self.rooms:
            print (index['id'])
            if index['id'] == room_id:
                index['player_names'].append(player_name)
                index['sockets'].append(client_room)
                room_name = index['room_name']
                host_name = index['host_name']
                client_room.send("joined succesfully".encode() + "R".encode() + room_name.encode() + "H".encode() + host_name.encode())
                check = True
                print("joined room")
                return True
        if check == False:
              client_room.send("failed to join not found room id".encode() + "I".encode() + str(room_id).encode())
              print("rejected to join")
              return False
                

    def createRoom(self,client_request,client_room,find_N):
        room_id = self.backend.generate_random_room_id(self.room_ids)
        self.room_ids.append(room_id)
        find_R = client_request.find("R")
        host_name = client_request[find_N + 1:find_R]
        room_name = client_request[find_R + 1:]
        # self.roomsNames.append([username])
        # self.roomsSockets.append([client_room])
        self.rooms.append(
            {
              "id": room_id,
              "host_name":host_name,
              "host_socket":client_room,
              "room_name": room_name,
              "player_names":[host_name],
              "sockets" :[client_room]
            }
        )
        print(self.rooms)
        client_room.send("room was created succesfully".encode() + "I".encode() + str(room_id).encode())
        self.room_num += 1
        print("room created!")
        print("there are " +str(self.room_num)+ " rooms")
        return True

    
        
if __name__ == '__main__':
   rooms = Rooms()
   rooms.main()