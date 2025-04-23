import random
from Generators.distractors_generator import DistractorsGenerator

class AlgbraBasicQG(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["whatx"])
        if self.question_type == "whatx":
            self.what_is_x()
        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
    
    def what_is_x(self):
        x = random.randint(2,10)
        multiplier = random.randint(2,10)
        addtion = random.randint(2,10)
        self.question_text = f"Solve the following equation for x\n{multiplier}x + {addtion} = {multiplier*x + addtion}"
        self.solution = f"x = {x}"
        self.distractors = self.distractors_generator(x, title="x =")

