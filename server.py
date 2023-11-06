import socket
import question_data
import select
import backend


class Server():
    
    def __init__(self,array_of_sockets,array_of_names):
        self.array_of_names = array_of_names
        self.array_of_sockets = array_of_sockets
        self.backend = backend.Backend(self,array_of_names)
        server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_socket1.bind(("0.0.0.0",8833))
        # server_socket1.listen()
        # print("socket1 is up and ready!")
        # (self.client_socket1,self.client_address1) = server_socket1.accept()
        # print("first client connected")
        # (self.client_socket2,self.client_address2) = server_socket1.accept()
        # print("secound client connected")
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
            # check1 = self.client_socket1.recv(1024).decode() 
            # check2 = self.client_socket2.recv(1024).decode() 
            print(checks)
            # print(check2)
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
    #    self.client_socket1.send("question".encode() + str(self.question_and_ans).encode())
    #    self.client_socket2.send("question".encode() + str(self.question_and_ans).encode())
    #    print("question sent")
        
        
            
            
    def waitForAnswers(self,array_of_answers):
              for answer in array_of_answers:
                answer = self.reciveTheFullServer_sent(15,answer)
                
            # answer1 = self.reciveTheFullServer_sent(15,answer1)
           
            # answer2 = self.reciveTheFullServer_sent(15,answer2)
              self.backend.check_answer(array_of_answers)
            #   self.backend.check_answer(0,answer1)
            #   self.backend.check_answer(1,answer2)        
              self.infoForClients()
                            
    def infoForClients(self):
        players_score = self.backend.get_score()
        # player1_score = self.backend.get_score(0)
        # player2_score = self.backend.get_score(1)
        counter = 0
        for x in players_score:
            my_score = players_score[counter]
            self.array_of_sockets[counter].send("info".encode() + str(my_score).encode() + "o".encode() + str(players_score).encode())
            counter += 1
            # self.client_socket1.send("info".encode() + "a".encode() + str(player1_score).encode() + "b".encode() + str(player2_score).encode())
            # self.client_socket2.send("info".encode() + "a".encode() + str(player2_score).encode() + "b".encode() + str(player1_score).encode())
        
       
        
# if __name__ == '__main__':
#     print("im here")
#     server = Server(array_of_sockets)
#     server.sendQuestion()
            
