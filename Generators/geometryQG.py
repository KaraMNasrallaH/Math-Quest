import random
import json

class GeometryQG:
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.question_type = []
        self.distractors = None
        

    def generate(self):
        self.geometry_info()
        return{
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
    
    def geometry_info(self):
        with open("geometry_questions.json", "r", encoding="utf-8") as file:
            questions = json.load(file)
        selected_question = random.choice(questions)
        self.question_text = selected_question["question"]
        self.solution = selected_question["solution"]
        self.distractors = selected_question["distractors"]

        
        
if __name__ == "__main__":
    test = GeometryQG()
    question_data = test.generate()
    print(question_data["question"])
    print(question_data["solution"])
    print(question_data["distractors"])
