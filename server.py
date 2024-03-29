import socket
import question_data
import select
import backend
import manage_games_server

class Server():
    
    def __init__(self,array_of_sockets,array_of_names,room_id):
        print("start")
        self.room_id = room_id
        self.array_of_names = array_of_names
        self.array_of_sockets = array_of_sockets
        self.backend = backend.Backend(self)
        self.backend.get_list_of_names(array_of_names)
        self.server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.question_and_ans = self.backend.next_question()
        # self.manage_games_server = manage_games_server.Rooms()
        self.game_over_flag = False
        counter = 1
        for x in self.array_of_sockets:
                # client_room = x
                # client_room.send("connected to server".encode())
                print("client " + str(counter) + " connected")
                counter += 1
        print("sentttt")
        self.sendQuestion()


    
        
    def main(self):
        while self.game_over_flag == False:
            flag = 0
            checks = []
            for client in self.array_of_sockets:
                checks.append(client.recv(1024).decode())
            for x in checks:
                check = x
                print(check)          
                if check[:15] != "selected answer":  
                    flag = 1
            if flag == 0:
               self.waitForAnswers(checks)
            else:   
                 flag = 0
                 for x in checks:
                     check = x   
                    
                     if check[:13] != "next question":
                            flag = 1
                     if flag == 0:
                        self.question_and_ans = self.backend.next_question()
                        self.sendQuestion()
            
                 
            
    def game_over(self,scores_array,winner_indexes_array):
        self.game_over_flag == True
        for socket in self.array_of_sockets:
            socket.send("game over".encode() + str(scores_array).encode() + "*".encode() + str(winner_indexes_array).encode())
            socket.close()
            print("client closed")
            self.server_socket1.close()
            # self.manage_games_server.delete_room(self.room_id)
        
    
    
    
    def reciveTheFullServer_sent(self,x,server_sent):
        server_sent = server_sent[x:]
        return server_sent

        
        
    def sendQuestion(self):
       counter = 1
       for client in self.array_of_sockets:
                client.send("question".encode() + str(self.question_and_ans).encode())
                print("question sent to client " + str(counter))
                counter += 1
       self.main()        
   
        
        
            
            
    def waitForAnswers(self,array_of_answers):
        counter = 0
        for answer in array_of_answers:
            array_of_answers[int(counter)] = self.reciveTheFullServer_sent(15,answer)
            counter += 1
        self.backend.check_answer(array_of_answers)    
        self.infoForClients()
                      
                      
                            
    def infoForClients(self):
        players_score = self.backend.get_score()
        if players_score == []:
            pass
        else:
            print(players_score)
            counter = 0
            for x in players_score:
                my_score = players_score[counter]
                self.array_of_sockets[counter].send("info".encode() + str(my_score).encode() + "o".encode() + str(players_score).encode())
                counter += 1
                print("answer sent to " + str(counter) +" clients")
            