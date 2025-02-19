import random

class FractionQG:
    """
    A class to generate fraction questions with solutions and distractors.
    Supported question types: addition/subtraction, multiplication, simplification, division, and conversion.
    """

    def __init__(self):
        self.question_type = ""
        self.question_text = ""
        self.solution = ""
        self.distractors = []

    def generate(self):
        """
        Randomly selects a question type and generates the corresponding question,
        solution, and distractor answers.

        Returns:
            A dictionary containing the question type, question text, solution, and distractors.
        """
        self.question_type = random.choice(
            ["addition/subtraction", "multiplication", "simplification", "division", "conversion"]
        )

        if self.question_type == "addition/subtraction":
            self.generate_addition_subtraction()
        elif self.question_type == "multiplication":
            self.generate_multiplication()
        elif self.question_type == "simplification":
            self.generate_simplification()
        elif self.question_type == "division":
            self.generate_division()
        elif self.question_type == "conversion":
            self.generate_fraction_conversion()

        return {
            "type": self.question_type,
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }

    def generate_addition_subtraction(self):
        """
        Generates a fraction addition or subtraction question along with its correct solution and distractors.

        Returns:
            A tuple containing the question text and the solution.
        """
        operator_symbol = random.choice(["+", "-"])
        a, b, c, d = (random.randint(1, 100) for _ in range(4))

        if operator_symbol == "+":
            correct_numer = a * d + c * b
            correct_denom = b * d
            self.solution = f"{correct_numer}/{correct_denom}"
            self.question_text = f"Calculate: {a}/{b} + {c}/{d} (using a common denominator)"
            # Common distractor mistakes:
            distractor1 = f"{a * d - c * b}/{b * d}"   # subtraction instead of addition
            distractor2 = f"{a * d + c * b}/{b + d}"     # adding denominators instead of multiplying
            distractor3 = f"{a * b + c * d}/{b * d}"     # mixing up multiplication
        else:
            correct_numer = a * d - c * b
            correct_denom = b * d
            self.solution = f"{correct_numer}/{correct_denom}"
            self.question_text = f"Calculate: {a}/{b} - {c}/{d} (using a common denominator)"
            # Distractor mistakes:
            distractor1 = f"{a * d + c * b}/{b * d}"     # using addition instead of subtraction
            distractor2 = f"{a * d - c * b}/{b + d}"       # wrong denominator: b+d instead of b*d
            distractor3 = f"{a * b - c * d}/{b * d}"       # mixing up multiplication

        
        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

    def generate_multiplication(self):
        """
        Generates a multiplication fraction question along with its solution and distractors.

        Returns:
            A tuple containing the question text and the solution.
        """
        a, b, c, d = (random.randint(1, 100) for _ in range(4))
        self.solution = f"{a * c}/{b * d}"
        self.question_text = f"Calculate: {a}/{b} x {c}/{d}"
        # Distractor mistakes:
        distractor1 = f"{a * c}/{b + d}"   # mistake: adding denominators instead of multiplying
        distractor2 = f"{a + c}/{b * d}"     # mistake: adding numerators instead of multiplying
        distractor3 = f"{a * d}/{b * c}"     # mistake: swapping one term in multiplication

        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

    def generate_simplification(self):
        """
        Generates a fraction simplification question. There's a 70% chance the fraction is simplifiable,
        and a 30% chance it's already in simplest form. Also generates distractors accordingly.

        Returns:
            A tuple containing the question text and the solution.
        """
        def find_gcd(x: int, y: int) -> int:
            """Return the greatest common divisor using Euclid's algorithm."""
            while y:
                x, y = y, x % y
            return x

        while True:
            a = random.randint(5, 150)
            b = random.randint(5, 150)
            gcd = find_gcd(a, b)

            # 70% chance for a simplifiable fraction
            if random.random() < 0.7:
                if gcd > 1:
                    simp_numer = a // gcd
                    simp_denom = b // gcd
                    self.solution = f"{simp_numer}/{simp_denom}"
                    self.question_text = f"Simplify this fraction: {a}/{b}"

                    # Distractor mistakes:
                    distractor1 = f"{a}/{b}"  # unsimplified version
                    distractor2 = f"{simp_denom}/{simp_numer}" if simp_numer != simp_denom else f"{simp_numer}/{simp_denom + 1}"
                    distractor3 = f"{simp_numer + 1}/{simp_denom}"  # off-by-one error in numerator
                    break
                
            # 30% chance for an already simplified fraction
            else:
                if gcd == 1:
                    self.solution = f"This fraction is already simplified: {a}/{b}"
                    self.question_text = f"Simplify this fraction: {a}/{b}"
                    
                    # Distractor mistakes:
                    distractor1 = f"This fraction is already simplified: {a}/{b+1}"
                    distractor2 = f"This fraction is already simplified: {a+1}/{b}"
                    distractor3 = f"This fraction is already simplified: {b}/{a}"
                    break

        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

    def generate_division(self):
        """
        Generates a fraction division question along with its correct solution and distractors.

        Returns:
            A tuple containing the question text and the solution.
        """
        a, b, c, d = (random.randint(1, 100) for _ in range(4))
        correct_answer = f"{a * d}/{b * c}"
        self.question_text = f"Calculate: {a}/{b} ÷ {c}/{d}"
        # Distractor mistakes:
        distractor1 = f"{(a * d) + 1}/{b * c}"  # small error in numerator
        distractor2 = f"{a * d}/{b + c}"         # wrong denominator operation
        distractor3 = f"{a + b}/{c + d}"          # completely different operation

        self.solution = correct_answer
        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

    def generate_fraction_conversion(self):
        """
        Generates a fraction-to-decimal conversion question with its correct solution and distractors.

        Returns:
            A tuple containing the question text and the solution.
        """
        denominator = random.randint(1, 1000)
        numerator = random.randint(1, denominator - 1)
        decimal = "0."
        self.question_text = f"Convert this fraction to a decimal: {numerator}/{denominator}"
        # Start conversion process by multiplying numerator by 10
        num = numerator * 10

        while True:
            # Pad with zeros if necessary
            while num < denominator:
                decimal += "0"
                num *= 10

            decimal += str(num // denominator)
            num %= denominator  # update remainder

            if num == 0:  # terminating decimal
                break

            if len(decimal) > 13:  # limit decimal length
                break

            num *= 10

        correct_decimal = decimal
        self.solution = correct_decimal

        # Distractor mistakes for conversion:
        if correct_decimal[-1].isdigit():
            last_digit = int(correct_decimal[-1])
            new_digit = (last_digit + 1) % 10
            distractor1 = correct_decimal[:-1] + str(new_digit)
        else:
            distractor1 = correct_decimal

        distractor2 = correct_decimal[:-1] if len(correct_decimal) > 3 else correct_decimal
        distractor3 = correct_decimal + str(random.randint(0, 9))

        self.distractors = [
            f"{distractor1}",
            f"{distractor2}",
            f"{distractor3}"
        ]
        return self.question_text, self.solution, self.distractors

# Example usage:
if __name__ == "__main__":
    fqg = FractionQG()
    question_data = fqg.generate()
    print("Question Type:", question_data["type"])
    print("Question:", question_data["question"])
    print("Solution:", question_data["solution"])
    print("Distractors:", question_data["distractors"])
