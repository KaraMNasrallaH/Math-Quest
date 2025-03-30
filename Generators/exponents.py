import math
import random
from collections import Counter

from Generators.distractors_generator import DistractorsGenerator

class ExponentsQG(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["simplest radical","hidden power"])
        if self.question_type == "simplest radical":
            self.simplest_radical()
        elif self.question_type == "hidden power":
            self.hidden_power()
        return {
            "question":self.question_text,
            "solution":self.solution,
            "distractors":self.distractors
                }

    def simplest_radical(self):
        prime_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                    53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                    113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
                    181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
                    251, 257, 263, 269, 271, 277, 281, 283, 293]

        root_index = random.randint(2, 5)
        exponent_symbol = ["²√","³√","⁴√","⁵√"]
        selected_symbol = exponent_symbol[root_index - 2]

        simplified_prob = random.random() < 0.8

        while True:
            a = random.randint(10, 300)
            if a in prime_nums:
                continue

            temp_a = a
            factors = []
            for prime in prime_nums:
                while temp_a % prime == 0:
                    factors.append(prime)
                    temp_a //= prime
                if temp_a == 1:
                    break

            factor_count = Counter(factors)
            simplification_found = any(count >= root_index for count in factor_count.values())

            if simplified_prob:
                if simplification_found:
                    break
            else:
                if not simplification_found:
                    break

        self.question_text = f"Find the simplest radical form for {selected_symbol}{a}"

        outside = 1
        inside = 1
        for prime, count in factor_count.items():
            out_count = count // root_index
            in_count = count % root_index
            if out_count:
                outside *= prime ** out_count
            if in_count:
                inside *= prime ** in_count

        if inside == 1:
            self.solution = str(outside)
            self.distractors = self.distractors_generator(outside)
        else:
            self.solution = f"{outside} {selected_symbol}{inside}"
            A_dis = self.distractors_generator(outside)
            self.distractors = [f"{a} {selected_symbol}{inside}" for a in A_dis]

    def hidden_power(self):
        a = random.randint(2,9)
        b = random.randint(0,5)
        self.question_text = f"If {a}^x = {a**b}, what is x?"
        self.solution = str(b)
        self.distractors = self.distractors_generator(b)

if __name__ == "__main__":
    test = ExponentsQG()
    question_data = test.generate()
    print(question_data["question"])
    print(question_data["solution"])
    print(question_data["distractors"])


            
            