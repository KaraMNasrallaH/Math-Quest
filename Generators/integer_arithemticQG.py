import random
from Generators.distractors_generator import DistractorsGenerator

class Integer_ArithmeticQG(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None

    def generate(self):
        self.question_type = random.choice(["Adding_subtracting", "Multiplication_division", "Absolute_value"])
        if self.question_type == "Adding_subtracting":
            self.adding_subtracting()
        elif self.question_type == "Multiplication_division":
            self.multiplication_division()
        elif self.question_type == "Absolute_value":
            self.abs_value()
        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
    
    def adding_subtracting(self):
        a = random.randint(-10,10)
        b = random.randint(-10,10)
        operator = random.choice(["-","+"])
        result = a + b if operator == "+" else a - b

        self.question_text = f"{a} {operator} {b}"
        self.solution = str(result)
        self.distractors = self.distractors_generator(result)

    def multiplication_division(self):
        a, b = 0, 0
        while a == 0 or b == 0:
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
        operator = random.choice(["/", "x"])
        result = a * b if operator == "x" else a / b
        result = round(result, 2) if isinstance(result, float) and not result.is_integer() else int(result)

        self.question_text = f"{a} {operator} {b}"
        self.solution = str(result)
        self.distractors = self.distractors_generator(result)

    def abs_value(self):
        a = random.randint(-10, 10)
        result = abs(a)
        self.question_text = f"|{a}|"
        self.solution = str(result)
        self.distractors = self.distractors_generator(result)

if __name__ == "__main__":
    test = Integer_ArithmeticQG()
    question_data = test.generate()
    print(question_data["question"])
    print(question_data["solution"])
    print(question_data["distractors"])
