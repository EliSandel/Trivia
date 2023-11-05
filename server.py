import socket
import question_data
import select
import backend


class Server():
    
    def __init__(self):
        self.backend = backend.Backend(self)
        server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket1.bind(("0.0.0.0",8833))
        server_socket1.listen()
        print("socket1 is up and ready!")
        (self.client_socket1,self.client_address1) = server_socket1.accept()
        print("first client connected")
        (self.client_socket2,self.client_address2) = server_socket1.accept()
        print("secound client connected")
        self.question_and_ans = self.backend.next_question()



    
        
    def main(self):
        while True:
            print("while")
            check1 = self.client_socket1.recv(1024).decode() 
            check2 = self.client_socket2.recv(1024).decode() 
            print(check1)
            print(check2)
            if check1 == "didnt got question":
                print("1")
                self.sendQuestion() 
            if check2 == "didnt got question":
                print("2")       
                self.sendQuestion()      
            
            if check1[:15] == "selected answer" and check2[:15] == "selected answer":  
                print("4")
                self.waitForAnswers(check1,check2)
            if check1[:13] == "next question" and  check2[:13] == "next question":
                print("5")
                self.question_and_ans = self.backend.next_question()
                self.sendQuestion()
            
                 
            
            
    def reciveTheFullServer_sent(self,x,server_sent):
        server_sent = server_sent[x:]
        return server_sent

        
        
    def sendQuestion(self):
       
        self.client_socket1.send("question".encode() + str(self.question_and_ans).encode())
        self.client_socket2.send("question".encode() + str(self.question_and_ans).encode())
        print("question sent")
        
        self.main()
        
            
            
    def waitForAnswers(self,answer1,answer2):
       
            answer1 = self.reciveTheFullServer_sent(15,answer1)
           
            answer2 = self.reciveTheFullServer_sent(15,answer2)
            
            self.backend.check_answer(0,answer1)
            self.backend.check_answer(1,answer2)        
            self.infoForClients()
                            
    def infoForClients(self):
        player1_score = self.backend.get_score(0)
        player2_score = self.backend.get_score(1)
        
        self.client_socket1.send("info".encode() + "a".encode() + str(player1_score).encode() + "b".encode() + str(player2_score).encode())
        self.client_socket2.send("info".encode() + "a".encode() + str(player2_score).encode() + "b".encode() + str(player1_score).encode())
        
       
        
if __name__ == '__main__':
    server = Server()
    server.sendQuestion()
            
            
