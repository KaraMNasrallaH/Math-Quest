import random
import json
import math

class GeometryQG:
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.question_type = []
        self.distractors = None
        
    def generate(self):
        self.question_type = random.choice(["geometry_info","find_perimeter"])
        if self.question_type == "geometry_info":
            self.geometry_info()
        elif self.question_type == "find_perimeter":
            self.find_perimeter()
        return{
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
    
    def distractors_generator(self, result, title=False):
        possible_offsets = list(range(1, 6))
        unique_offsets = random.sample(possible_offsets, 3)
        if title:
            distractors = [f"{title}: {result + offset}" for offset in unique_offsets]
        else:
            distractors = [str(round(result + offset, 2)) if isinstance(result, float) else str(result + offset) for offset in unique_offsets]
        return distractors
        
    def geometry_info(self):
        with open("geometry_questions.json", "r", encoding="utf-8") as file:
            questions = json.load(file)
        selected_question = random.choice(questions)
        self.question_text = selected_question["question"]
        self.solution = selected_question["solution"]
        self.distractors = selected_question["distractors"]

    def find_perimeter(self):
        shape = random.choice(["square","rectangle","triangle","circle"])
        if shape == "square":
            a = random.randint(1,10)
            if random.random() > 0.5:
                self.question_text = f"A square has a side length of {a} cm. What is its perimeter"
                result = a*4
            else:
                self.question_text = f"A regular pentagon has a side of {a} cm. What is its perimeter"
                result = a*5

        elif shape == "rectangle":
            a = random.randint(10,20)
            b = random.randint(5,a-2)
            self.question_text = f"A rectangle has a length of {b} cm and a width of {a} cm. What is its perimeter"
            result = a*2+b*2

        elif shape == "triangle":
            a,b,c = (random.randint(3,15) for _ in range(3))
            self.question_text = f"A triangle has sides measuring {a} cm, {b} cm, and {c} cm. What is its perimeter"
            result = a+b+c

        elif shape == "circle":
            a = random.randint(3,10)
            self.question_text = f"If a circle has a radius of {a} cm, what is its circumference"
            result = a*2*math.pi
        self.solution = str(round(result, 2)) if isinstance(result, float) and not result.is_integer() else str(int(result))
        self.distractors = self.distractors_generator(result)

        
        
if __name__ == "__main__":
    test = GeometryQG()
    question_data = test.generate()
    print(question_data["question"])
    print(question_data["solution"])
    print(question_data["distractors"])
