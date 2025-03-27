import random
from math import gcd as find_gcd
from Generators.distractors_generator import DistractorsGenerator

class MixedNumbersQG(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["conversion", "subtraction", "simplification"])
        
        if self.question_type == "subtraction":
            self.generate_subtraction()
        elif self.question_type == "conversion":
            self.generate_conversion()
        elif self.question_type == "simplification":
            self.generate_simplification()
        
        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }

    def generate_subtraction(self):
        n1 = random.randint(16,30)
        d1 = random.randint(2,6)
        n2 = random.randint(10,17)
        d2 = random.randint(5,11)
        # Generate two mixed numbers
        whole1, rem1 = n1 // d1, n1 % d1
        whole2, rem2 = n2 // d2, n2 % d2
        self.question_text = (
            f"Subtract the mixed numbers: {whole1} {rem1}/{d1}  -  {whole2} {rem2}/{d2}"
        )

        common_gcd = find_gcd(d1, d2)
        lcd = (d1 * d2) // common_gcd
        scalednumer1 = n1 * (lcd // d1)
        scalednumer2 = n2 * (lcd // d2)
        result = scalednumer1 - scalednumer2
        self.solution = f"{int(result/lcd)} {abs(result) % lcd}/{lcd}"
        
        # Distractors that reflect common mistakes:
        distractor1 = f"{int(result/lcd + 1)} {abs(result) % lcd}/{lcd}"
        distractor2 = f"{int(result/lcd)} {abs(result + 1) % lcd}/{lcd}"
        distractor3 = f"{int(result/lcd)} {abs(result) % lcd}/{lcd + 1}"
        self.distractors = [distractor1, distractor2, distractor3]

    def generate_conversion(self):
        n1 = random.randint(7, 20)
        d1 = random.randint(2, 10)
        if random.random() < 0.5:
            # Convert improper fraction to mixed number
            self.question_text = f"Convert the improper fraction {n1}/{d1} into a mixed number."
            self.solution = f"{n1//d1} {n1%d1}/{d1}"
            distractor1 = f"{n1//d1 + 3} {n1%d1}/{d1}"
            distractor2 = f"{n1//d1} {n1%d1 + 1}/{d1}"
            distractor3 = f"{n1//d1} {(n1 + 1) % d1}/{d1}"
        else:
            # Convert mixed number to improper fraction
            whole = n1 // d1
            rem = n1 % d1
            self.question_text = f"Convert the mixed number {whole} {rem}/{d1} into an improper fraction."
            self.solution = f"{n1}/{d1}"
            distractor1 = f"{n1 + 1}/{d1}"
            distractor2 = f"{n1}/{d1 + 2}"
            distractor3 = f"{n1 + 1}/{d1 - 1}"

        self.distractors = [distractor1, distractor2, distractor3]
   
    def generate_simplification(self):
        whole = random.randint(1, 10)
        n1 = random.randint(1, 30)
        d1 = random.randint(1, 10)
        self.question_text = f"Simplify the mixed number {whole} {n1}/{d1}."

        # Convert mixed number to improper fraction
        improper = whole * d1 + n1
        common_gcd = find_gcd(improper, d1)
        simplified_numer = improper // common_gcd
        simplified_denom = d1 // common_gcd

        # Convert back to mixed number format
        self.solution = f"{simplified_numer // simplified_denom} {simplified_numer % simplified_denom}/{simplified_denom}"
        distractor1 = f"{simplified_numer // simplified_denom + 1} {simplified_numer % simplified_denom}/{simplified_denom}"
        distractor2 = f"{simplified_numer // simplified_denom} {simplified_numer % simplified_denom}/{simplified_denom + 1}"
        distractor3 = f"{simplified_numer // simplified_denom} {(simplified_numer % simplified_denom) + 1}/{simplified_denom}"
        self.distractors = [distractor1, distractor2, distractor3]

if __name__ == "__main__":
    test = MixedNumbersQG()
    question_data = test.generate()
    print("Question:", question_data["question"])
    print("Solution:", question_data["solution"])
    print("Distractors:", question_data["distractors"])
