import random
from Generators.distractors_generator import DistractorsGenerator

class Measurement(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["calculate_distance"])
        if self.question_type == "calculate_distance":
            self.calculate_distance()
        
        return {"question": self.question_text,
                "solution": self.solution,
                "distractors": self.distractors}
    
    def calculate_distance(self):
        meters = random.randint(100,200)
        km = random.randint(40,80)
        self.question_text = f"A train is {meters} meters long and travels at a constant speed of {km} km/h.\nHow long (in seconds) does it take the train to completely pass a signpost?"
        speed = (km * 1000) / 3600
        result = round(meters / speed, 2)
        self.solution = f"{result} seconds"
        A_dis = self.distractors_generator(result)
        self.distractors = [f"{a} seconds" for a in A_dis]

