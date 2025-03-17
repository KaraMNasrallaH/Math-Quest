import random

class RatiosANDProportionQG:
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["ratio","ratio_part"])
        
        if self.question_type == "ratio":
            self.ratio()
        elif self.question_type == "ratio_part":
            self.ratio_part()

        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
    
    def ratio(self):
        ratio_A = random.randint(2, 20)
        ratio_B = random.randint(2, 30)
        total_parts = ratio_A + ratio_B
        multiplier = random.randint(2, 20)
        total = total_parts * multiplier
        
        self.question_text = (f"The ratio of red to blue marbles is {ratio_A}:{ratio_B}.\n"
                              f"If total marbles is {total}, how many red and blue marbles are there?")
        
        result = total // total_parts
        correct_red = result * ratio_A
        correct_blue = result * ratio_B
        self.solution = f"Red: {correct_red}, Blue: {correct_blue}"
        self.distractors = [
            f"Red: {result * ratio_B}, Blue: {result * ratio_A}",
            f"Red: {result * (ratio_A + 1)}, Blue: {result * (ratio_B - 1)}",
            f"Red: {round(total / ratio_A)}, Blue: {round(total / ratio_B)}"
        ]
    
    def ratio_part(self):
        ratio_A = random.randint(2, 20)
        ratio_B = random.randint(2, 30)
        total_parts = ratio_A + ratio_B
        multiplier = random.randint(2, 20)
        total = total_parts * multiplier
        result = total // total_parts
        correct_apples = result * ratio_A
        correct_oranges = result * ratio_B

        self.question_text = (f"In a basket, the ratio of apples to oranges is {ratio_A}:{ratio_B}.\n"
                              f"If there are {correct_apples} apples, how many oranges are there?")
        self.solution = f"{correct_oranges}"
        self.distractors = [
            f"{correct_oranges + result}",
            f"{result * (ratio_B - 1)}",
            f"{result * (ratio_B + 2)}"
        ]
