import random
from Generators.distractors_generator import DistractorsGenerator

class MeasurementQG(DistractorsGenerator):
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
        question_type = random.choice([("train", "seconds"), ("space", "m/s"), ("race", "seconds")])

        if question_type[0] == "train":
            meters = random.randint(100, 200)
            km = random.randint(40, 80)
            self.question_text = f"A train is {meters} meters long and travels at a constant speed of {km} km/h.\nHow long (in seconds) does it take the train to completely pass a signpost?"
            speed = (km * 1000) / 3600
            result = round(meters / speed, 2)

        elif question_type[0] == "space":
            meters = random.randint(40000, 50000)
            time = int(random.randint(4, 8) / 2)
            self.question_text = f"A Mars rover travels {meters} meters in {time} hours.\nWhat is its speed in meters per second (m/s)?"
            result = round(meters / (time * 3600), 2)
        
        elif question_type[0] == "race":
            turtle_speed = random.randint(2, 9) / 10
            rabbit_speed = random.randint(21, 49) / 10
            pausing_time = random.randint(3, 10)
            self.question_text = f"A turtle starts walking at {turtle_speed} m/s. {pausing_time} minutes later,\na rabbit starts chasing it from the same starting point, running at {rabbit_speed} m/s.\nHow long (in seconds) after the rabbit starts will it catch the turtle?"
            relative_speed = rabbit_speed - turtle_speed
            turtle_passed = (turtle_speed * (pausing_time * 60))
            result = round(turtle_passed / relative_speed, 2)
        
        self.solution = f"{result} {question_type[1]}"
        A_dis = self.distractors_generator(result)
        self.distractors = [f"{a} {question_type[1]}" for a in A_dis]
    

