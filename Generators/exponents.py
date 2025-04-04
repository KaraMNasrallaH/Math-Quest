import math
import random
from collections import Counter

from Generators.distractors_generator import DistractorsGenerator

class ExponentsQG(DistractorsGenerator):
    def __init__(self):
        # Initialize attributes to store the question, solution, and distractors
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        # Randomly choose between two types of exponent-related questions
        self.question_type = random.choice(["scientific notation"])
        
        if self.question_type == "simplest radical":
            self.simplest_radical()
        elif self.question_type == "hidden power":
            self.hidden_power()
        elif self.question_type == "scientific notation":
            self.scientific_notation()
        
        # Return the generated question, solution, and distractors
        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }

    def simplest_radical(self):
        # List of prime numbers for factorization
        prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                        53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                        113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
                        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
                        251, 257, 263, 269, 271, 277, 281, 283, 293]

        # Choose a random root index (square root, cube root, etc.)
        root_degree = random.randint(2, 5)
        radical_symbols = ["²√", "³√", "⁴√", "⁵√"]
        radical_symbol = radical_symbols[root_degree - 2]

        # 80% chance to select a number that simplifies
        is_simplifiable = random.random() < 0.8

        while True:
            radicand = random.randint(10, 300)
            if radicand in prime_numbers:  # Skip prime numbers
                continue

            # Factorize the number
            remaining_value = radicand
            factors = []
            for prime in prime_numbers:
                while remaining_value % prime == 0:
                    factors.append(prime)
                    remaining_value //= prime
                if remaining_value == 1:
                    break

            # Count occurrences of each prime factor
            factor_counts = Counter(factors)
            
            # Check if simplification is possible
            can_simplify = any(count >= root_degree for count in factor_counts.values())

            # Select number based on whether we want a simplifiable or non-simplifiable one
            if is_simplifiable and can_simplify:
                break
            elif not is_simplifiable and not can_simplify:
                break

        # Generate the question
        self.question_text = f"Find the simplest radical form for {radical_symbol}{radicand}"

        # Compute the simplified radical form
        coefficient = 1  # Number outside the radical
        remaining_radicand = 1  # Number inside the radical
        for prime, count in factor_counts.items():
            outside_exponent = count // root_degree  # Part that goes outside the radical
            inside_exponent = count % root_degree   # Part that stays inside

            if outside_exponent:
                coefficient *= prime ** outside_exponent
            if inside_exponent:
                remaining_radicand *= prime ** inside_exponent

        # If there's nothing left inside the radical
        if remaining_radicand == 1:
            self.solution = str(coefficient)
            self.distractors = self.distractors_generator(coefficient)
        else:
            self.solution = f"{coefficient} {radical_symbol}{remaining_radicand}"
            distractor_values = self.distractors_generator(coefficient)
            self.distractors = [f"{d} {radical_symbol}{remaining_radicand}" for d in distractor_values]

    def hidden_power(self):
        # Generate a simple exponent equation
        a = random.randint(2, 9)
        b = random.randint(0, 5)

        # Create the question
        self.question_text = f"If {a}^x = {a**b}, what is x?"
        self.solution = str(b)

        # Generate distractors
        self.distractors = self.distractors_generator(b)

    def scientific_notation(self):
        base = random.randint(100, 999)
        exponent = random.randint(-6, 10)
        question_type = random.choice(["write", "convert", "multi-divide"])

        if question_type == "write":
            standard_form = base * (10 ** exponent)
            if standard_form >= 1:
                sci_exponent = len(str(int(standard_form))) - 1
                sci_coefficient = standard_form / (10 ** sci_exponent)
            else:
                sci_exponent = 0
                sci_coefficient = standard_form
                while abs(sci_coefficient) < 1:
                    sci_coefficient *= 10
                    sci_exponent -= 1

            sci_coefficient_str = f"{sci_coefficient:.3g}"

            self.question_text = f"Write {standard_form:,} in scientific notation"
            self.solution = f"{sci_coefficient_str} x 10^{sci_exponent}"

            distractor_exponents = self.distractors_generator(sci_exponent)
            self.distractors = [
                f"{sci_coefficient_str} x 10^{exp}"
                for exp in distractor_exponents
            ]
        elif question_type == "convert":
            self.question_text = f"Convert {base} x 10^{exponent} to standard form"
            standard_form = base * (10 ** exponent)
            self.solution = f"{standard_form:,}"
            self.distractors = [
                f"{base * (10 ** (exponent - 1)):,}",
                f"{(base + 1) * (10 ** exponent):,}",
                f"{base * (10 ** (exponent + 1)):,}"
            ]
        elif question_type == "multi-divide":
            a, b, c, d = (random.randint(2, 10) for _ in range(4))

            if random.random() <= 0.5:
                self.question_text = f"What is ({a} x 10^{b}) / ({c} x 10^{d})?"

                coefficient = a / c
                coefficient = round(coefficient, 2) if not coefficient.is_integer() else int(coefficient)
                
                self.solution = f"{coefficient} x 10^{b - d}"
                self.distractors = [
                    f"{coefficient} x 10^{b + d}",
                    f"{round(c / a, 2)} x 10^{b - d}",
                    f"{coefficient} x 10^{d - b}" 
                ]

            else:
                self.question_text = f"What is ({a} x 10^{b}) x ({c} x 10^{d})?"
                self.solution = f"{a * c} x 10^{b + d}"
                self.distractors = [
                    f"{a * c} x 10^{b - d}",
                    f"{a + c} x 10^{b + d}",
                    f"{a * c} x 10^{b * d}"
                ]




if __name__ == "__main__":
    # Test the ExponentsQG class by generating a question
    test = ExponentsQG()
    question_data = test.generate()
    
    # Print the generated question, solution, and distractors
    print(question_data["question"])
    print(question_data["solution"])
    print(question_data["distractors"])


            
            