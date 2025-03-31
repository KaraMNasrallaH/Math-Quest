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
        self.question_type = random.choice(["simplest radical", "hidden power"])
        
        if self.question_type == "simplest radical":
            self.simplest_radical()
        elif self.question_type == "hidden power":
            self.hidden_power()
        
        # Return the generated question, solution, and distractors
        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }

    def simplest_radical(self):
        # List of prime numbers for factorization
        prime_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                      53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                      113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
                      181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
                      251, 257, 263, 269, 271, 277, 281, 283, 293]

        # Choose a random root index (square root, cube root, etc.)
        root_index = random.randint(2, 5)
        exponent_symbol = ["²√", "³√", "⁴√", "⁵√"]
        selected_symbol = exponent_symbol[root_index - 2]

        # 80% chance to select a number that simplifies
        simplified_prob = random.random() < 0.8

        while True:
            a = random.randint(10, 300)
            if a in prime_nums:  # Skip prime numbers
                continue

            # Factorize the number
            temp_a = a
            factors = []
            for prime in prime_nums:
                while temp_a % prime == 0:
                    factors.append(prime)
                    temp_a //= prime
                if temp_a == 1:
                    break

            # Count occurrences of each prime factor
            factor_count = Counter(factors)
            
            # Check if simplification is possible
            simplification_found = any(count >= root_index for count in factor_count.values())

            # Select number based on whether we want a simplifiable or non-simplifiable one
            if simplified_prob and simplification_found:
                break
            elif not simplified_prob and not simplification_found:
                break

        # Generate the question
        self.question_text = f"Find the simplest radical form for {selected_symbol}{a}"

        # Compute the simplified radical form
        outside = 1
        inside = 1
        for prime, count in factor_count.items():
            out_count = count // root_index  # Part that goes outside the radical
            in_count = count % root_index   # Part that stays inside

            if out_count:
                outside *= prime ** out_count
            if in_count:
                inside *= prime ** in_count

        # If there's nothing left inside the radical
        if inside == 1:
            self.solution = str(outside)
            self.distractors = self.distractors_generator(outside)
        else:
            self.solution = f"{outside} {selected_symbol}{inside}"
            A_dis = self.distractors_generator(outside)
            self.distractors = [f"{a} {selected_symbol}{inside}" for a in A_dis]

    def hidden_power(self):
        # Generate a simple exponent equation
        a = random.randint(2, 9)
        b = random.randint(0, 5)

        # Create the question
        self.question_text = f"If {a}^x = {a**b}, what is x?"
        self.solution = str(b)

        # Generate distractors
        self.distractors = self.distractors_generator(b)

if __name__ == "__main__":
    # Test the ExponentsQG class by generating a question
    test = ExponentsQG()
    question_data = test.generate()
    
    # Print the generated question, solution, and distractors
    print(question_data["question"])
    print(question_data["solution"])
    print(question_data["distractors"])


            
            