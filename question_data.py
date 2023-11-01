import requests
import html

#this class return a list with questions. each item in the list is a dict that has a question, right answer, wrong answers[], all answers[]

class TriviaApi:
    def __init__(self):
        self.api_url = "https://opentdb.com/api.php"
        self.all_questions = []
        pass


    def get_trivia_questions(self, amount=10, question_type="multiple", difficulty="easy"):

        # Define parameters for the API request
        params = {
            "amount": amount,  # Number of questions you want
            "type": question_type,  # You can specify "multiple" for multiple-choice questions or "boolean" for true/false questions
            "difficulty": difficulty
        }

        # Make the API request
        response = requests.get(self.api_url, params=params)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        self.all_questions=[]

        # Extract and display the questions and answers
        for question in data['results']:
            current_question = html.unescape(question['question'])
            correct_answer = question['correct_answer']
            incorrect_answers = question['incorrect_answers']
            all_answers = incorrect_answers.copy()
            all_answers.append(correct_answer)
            self.all_questions.append(
                {'question': current_question, 
                    'correct_answer': correct_answer, 
                    'incorrect_answers': incorrect_answers, 
                    'all_answers': all_answers
                }
            )
        return self.all_questions
  
    
