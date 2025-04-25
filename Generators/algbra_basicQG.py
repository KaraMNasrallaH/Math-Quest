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
    
    def exponents_laws(self):
        num = random.randint(1, 10)
        expo = random.randint(-5, 5)
        self.question_text = f"Simplify: {num}^{expo}"
        if expo == 0:
            self.solution = "1"
            self.distractors = self.distractors_generator(1)
        elif expo == 1:
            self.solution = f"{num}"
            self.distractors = self.distractors_generator(num)
        elif expo < 0:
            result = 1/num**(expo*-1)
            self.solution = f"{result}"
        else:
            question_type = random.choice(["pow_of_pow", "same_base", "diff_base"])
            operator = ["x", "/"]
            if question_type == "pow_of_pow":
                outter_expo = random.randint(1, 10)
                self.question_text = f"Simplify: ({num}^{expo})^{outter_expo}"
                result = expo * outter_expo
                self.solution = f"{num}^{result}"

            elif question_type == "same_base":
                expo2 = random.randint(1, 5)
                self.question_text = f"Simplify: x^{expo} {operator} x^{expo2}"
                if operator == "x":
                    result = expo + expo2
                    self.solution = f"x^{result}"
                elif operator == "/":
                    result = expo - expo2
                    self.solution = f"{result}" if result > 0 else f"1 / x^{(result*-1)}"

            elif question_type == "diff_base":
                base1 = "x"
                base2 = "y"
                if operator == "x":
                    self.question_text = f"Simplify: ({base1}{base2})^{expo}"
                    self.solution = f"{base1}^{expo} {base2}^{expo}"
                elif operator == "/":
                    self.question_text = f"Simplify: ({base1}/{base2})^{expo}"
                    self.solution = f"{base1}^{expo} / {base2}^{expo}"









        

