import random
from Generators.distractors_generator import DistractorsGenerator

class AlgebraBasicQG(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["whatx", "exponents_laws"])
        if self.question_type == "whatx":
            self.what_is_x()
        elif self.question_type == "exponents_laws":
            self.exponents_laws()
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
        self.distractors = self.distractors_generator(x, title="x = ")
    
    def exponents_laws(self):
        num = random.randint(1, 10)
        expo = random.randint(-3, 5)
        self.question_text = f"Simplify: {num}^{expo}"
        if expo == 0:
            self.solution = "1"
            self.distractors = self.distractors_generator(1)

        elif expo == 1:
            self.solution = f"{num}"
            self.distractors = self.distractors_generator(num)

        elif expo < 0:
            self.solution = f"1 / {num}^{-expo}"
            self.distractors = [
                f"{num}^{-expo}",
                f"1 / {num}^{-expo + 1}",
                f"1 / {num + 1}^{-expo}",
            ]
        else:
            question_type = random.choice(["pow_of_pow", "same_base"])
            if question_type == "pow_of_pow":
                outter_expo = random.randint(1, 10)
                self.question_text = f"Simplify: ({num}^{expo})^{outter_expo}"
                result = expo * outter_expo
                self.solution = f"{num}^{result}"
                A_dis = self.distractors_generator(num)
                B_dis = self.distractors_generator(result)
                self.distractors = [f"{a}^{b}" for a, b in zip(A_dis, B_dis)]

            elif question_type == "same_base":
                expo2 = random.randint(1, 5)
                op = random.choice(["*", "/"])
                self.question_text = f"Simplify: x^{expo} {op} x^{expo2}"
                result = expo + expo2 if op == "*" else expo - expo2

                if result == 0:
                    self.solution = "1"
                    self.distractors = self.distractors_generator(1)
                elif result > 0:
                    self.solution = f"x^{result}"
                    self.distractors = self.distractors_generator(result, title="x^")
                else:
                    abs_r = -result
                    self.solution = f"1 / x^{abs_r}"
                    self.distractors = self.distractors_generator(abs_r, title="1 / x^")










        

