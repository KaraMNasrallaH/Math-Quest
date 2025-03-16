import random

class PercentsQG:
    def __init__(self):
        # Initialize attributes
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate_distractors(self, result, is_percent=False):
        # Generate 3 unique offsets (excluding 0) and apply them
        offsets = random.sample([x for x in range(-5, 6) if x != 0], 3)
        distractors = [result + offset for offset in offsets]
        return [f"{d}%" for d in distractors] if is_percent else [str(d) for d in distractors]

    def generate(self):
        # Choose a random question type and generate the question
        self.question_type = random.choice(["find_part", "find_percentage", "find_total", "percentage_change"])
        if self.question_type == "find_part":
            self.find_part()
        elif self.question_type == "find_percentage":
            self.find_percentage()
        elif self.question_type == "find_total":
            self.find_total()
        elif self.question_type == "percentage_change":
            self.percentage_change()
        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
    
    def find_part(self):
        total = random.randint(1, 500)
        percent = random.randint(1, 100)
        self.question_text = f"What is {percent}% of {total}?"
        result = round(total * percent / 100)
        self.solution = f"{result}"
        self.distractors = self.generate_distractors(result)
    
    def find_percentage(self):
        total = random.randint(1, 500)
        part = random.randint(1, 100)
        self.question_text = f"What percent is {part} of {total}?"
        result = round(part / total * 100)
        self.solution = f"{result}%"
        self.distractors = self.generate_distractors(result, is_percent=True)
    
    def find_total(self):
        part = random.randint(1, 100)
        percent = random.randint(1, 100)
        self.question_text = f"If {part} is {percent}%, then what is the total?"
        result = round((part * 100) / percent)
        self.solution = f"{result}"
        self.distractors = self.generate_distractors(result)
    
    def percentage_change(self):
        original = random.randint(1, 200)
        new = random.randint(1, 400)
        self.question_text = f"What is the percent change if the original is {original} and the new is {new}?"
        change = new - original
        result = round((change / original) * 100)
        self.solution = f"{result}%"
        self.distractors = self.generate_distractors(result, is_percent=True)

if __name__ == "__main__":
    test = PercentsQG()
    question_data = test.generate()
    print("Question:", question_data["question"])
    print("Solution:", question_data["solution"])
    print("Distractors:", question_data["distractors"])


