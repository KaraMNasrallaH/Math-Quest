import random
import json
import math
from Generators.distractors_generator import DistractorsGenerator


class GeometryQG(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.question_type = []
        self.distractors = None
        
    def generate(self):
        self.question_type = random.choice(["geometry_info","find_perimeter","angle_relation","find_area"])
        self.shape = random.choice(["square","rectangle","triangle","circle"])
        if self.question_type == "geometry_info":
            self.geometry_info()
        elif self.question_type == "find_perimeter":
            self.find_perimeter()
        elif self.question_type == "angle_relation":
            self.angle_relation()
        elif self.question_type == "find_area":
            self.find_area()
        return{
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
        
    def geometry_info(self):
        with open("Generators//geometry_questions.json", "r", encoding="utf-8") as file:
            questions = json.load(file)
        selected_question = random.choice(questions)
        self.question_text = selected_question["question"]
        self.solution = selected_question["solution"]
        self.distractors = selected_question["distractors"]

    def find_perimeter(self):
        if self.shape == "square":
            a = random.randint(1,10)
            if random.random() > 0.5:
                self.question_text = f"A square has a side length of {a} cm. What is its perimeter"
                result = a*4
            else:
                self.question_text = f"A regular pentagon has a side of {a} cm. What is its perimeter"
                result = a*5

        elif self.shape == "rectangle":
            a = random.randint(10,20)
            b = random.randint(5,a-2)
            self.question_text = f"A rectangle has a length of {b} cm and a width of {a} cm. What is its perimeter"
            result = a*2+b*2

        elif self.shape == "triangle":
            a,b,c = (random.randint(3,15) for _ in range(3))
            self.question_text = f"A triangle has sides measuring {a} cm, {b} cm, and {c} cm. What is its perimeter"
            result = a+b+c

        elif self.shape == "circle":
            a = random.randint(3,10)
            self.question_text = f"If a circle has a radius of {a} cm, what is its circumference"
            result = a*2*math.pi
        self.solution = str(round(result, 2)) if isinstance(result, float) and not result.is_integer() else str(int(result))
        self.distractors = self.distractors_generator(result)
    
    def angle_relation(self):
        angle_type = random.choice(["complementary","supplementary"])
        if angle_type == "complementary":
            a = random.randint(10,50)
            result = 90 - a
        else:
            a = random.randint(40,140)
            result = 180 - a
        self.question_text = f"Two angles are {angle_type}. If one is {a}°, find the other"
        self.solution = f"{result}°"
        A_dis = self.distractors_generator(result)
        self.distractors = [f"{angle}°" for angle in A_dis]
    
    def find_area(self):
        a = random.randint(5, 10) * 2
        b = random.randint(5, 10)
        if self.shape == "triangle":
            self.question_text = f"The base of a triangle is {a} cm, and its height is {b} cm. Find the area."
            result = int((a*b) /2)
        elif self.shape == "square":
            self.question_text = f"A square has a side length of {a} cm. What is its area"
            result = a*a
        elif self.shape == "rectangle":
            self.question_text = f"A rectangle has a length of {a} cm and a width of {b} cm. What is its area?"
            result = a*b
        elif self.shape == "circle":
            self.question_text = f"A circle has a diameter of {a} cm. What is its area?"
            radius = a/2
            result = round((radius * radius) * math.pi,2)

        self.solution = f"{result} cm\u00B2"
        A_dis = self.distractors_generator(result)
        self.distractors = [f"{a} cm\u00B2" for a in A_dis]




        
        
if __name__ == "__main__":
    test = GeometryQG()
    question_data = test.generate()
    print(question_data["question"])
    print(question_data["solution"])
    print(question_data["distractors"])
