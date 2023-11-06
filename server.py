import socket
import question_data
import select
import backend


class Server():
    
    def __init__(self,array_of_sockets,array_of_names):
        self.array_of_names = array_of_names
        self.array_of_sockets = array_of_sockets
        print(array_of_names)
        self.backend = backend.Backend(self,array_of_names)
        server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.question_and_ans = self.backend.next_question()
        counter = 1
        for x in self.array_of_sockets:
                client_room = x
                client_room.send("connected to server".encode())
                print("client " + str(counter) + " connected")
                counter += 1
        self.sendQuestion()


    
        
    def main(self):
        print("main func")
        while True:
            flag = 0
            checks = []
            print("while")
            for client in self.array_of_sockets:
                checks.append(client.recv(1024).decode())
            print(checks)
            for x in checks:
                check = x
                                
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
            
                 
            
            
    def reciveTheFullServer_sent(self,x,server_sent):
        server_sent = server_sent[x:]
        return server_sent

        
        
    def sendQuestion(self):
       print("send question func")
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
              print(array_of_answers)
              self.backend.check_answer(array_of_answers)    
              self.infoForClients()
                            
    def infoForClients(self):
        players_score = self.backend.get_score()
        counter = 0
        print(players_score)
        for x in players_score:
            my_score = players_score[counter]
            print("forit")
            print(counter)
            print(my_score)
            self.array_of_sockets[counter].send("info".encode() + str(my_score).encode() + "o".encode() + str(players_score).encode())
            counter += 1
            print("answer sent to " + str(counter) +" clients")
            