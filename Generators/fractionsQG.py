import random

class FractionQG:
    """
    Generates fraction questions with solutions and distractors.
    Supported types: addition/subtraction, multiplication, simplification, division, and conversion.
    """

    def __init__(self):
        self.question_type = ""
        self.question_text = ""
        self.solution = ""
        self.distractors = []

    def generate(self):
        """
        Randomly selects a question type, generates the question, its solution, and distractors.
        Returns:
            dict: Contains question type, question text, solution, and distractors.
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
        Generates an addition or subtraction fraction question.
        Returns:
            tuple: (question text, solution, distractors)
        """
        operator_symbol = random.choice(["+", "-"])
        a, b, c, d = (random.randint(1, 100) for _ in range(4))

        if operator_symbol == "+":
            correct_numer = a * d + c * b
            correct_denom = b * d
            self.solution = f"{correct_numer}/{correct_denom}"
            self.question_text = f"Calculate: {a}/{b} + {c}/{d}"
            distractor1 = f"{a * d - c * b}/{b * d}"   # subtraction error
            distractor2 = f"{a * d + c * b}/{b + d}"     # wrong denominator (adding instead of multiplying)
            distractor3 = f"{a * b + c * d}/{b * d}"     # mixing multiplication operations
        else:
            correct_numer = a * d - c * b
            correct_denom = b * d
            self.solution = f"{correct_numer}/{correct_denom}"
            self.question_text = f"Calculate: {a}/{b} - {c}/{d}"
            distractor1 = f"{a * d + c * b}/{b * d}"     # addition error
            distractor2 = f"{a * d - c * b}/{b + d}"       # wrong denominator
            distractor3 = f"{a * b - c * d}/{b * d}"       # mixing multiplication operations

        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

    def generate_multiplication(self):
        """
        Generates a multiplication fraction question.
        Returns:
            tuple: (question text, solution, distractors)
        """
        a, b, c, d = (random.randint(1, 100) for _ in range(4))
        self.solution = f"{a * c}/{b * d}"
        self.question_text = f"Calculate: {a}/{b} x {c}/{d}"
        distractor1 = f"{a * c}/{b + d}"   # added denominators
        distractor2 = f"{a + c}/{b * d}"     # added numerators
        distractor3 = f"{a * d}/{b * c}"     # swapped terms

        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

    def generate_simplification(self):
        """
        Generates a fraction simplification question.
        Returns:
            tuple: (question text, solution, distractors)
        """
        def find_gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        while True:
            a = random.randint(5, 150)
            b = random.randint(5, 150)
            gcd = find_gcd(a, b)

            if random.random() < 0.7:  # generate a simplifiable fraction
                if gcd > 1:
                    simp_numer = a // gcd
                    simp_denom = b // gcd
                    self.solution = f"{simp_numer}/{simp_denom}"
                    self.question_text = f"Simplify this fraction: {a}/{b}"
                    distractor1 = f"{a}/{b}"  # unsimplified
                    distractor2 = f"{simp_denom}/{simp_numer}" if simp_numer != simp_denom else f"{simp_numer}/{simp_denom + 1}"
                    distractor3 = f"{simp_numer + 1}/{simp_denom}"  # off-by-one error
                    break
            else:  # fraction is already simplified
                if gcd == 1:
                    self.solution = f"{a}/{b}"
                    self.question_text = f"Simplify this fraction: {a}/{b}"
                    distractor1 = f"{a}/{b+1}"
                    distractor2 = f"{a+1}/{b}"
                    distractor3 = f"{b}/{a}"
                    break

        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

    def generate_division(self):
        """
        Generates a division fraction question.
        Returns:
            tuple: (question text, solution, distractors)
        """
        a, b, c, d = (random.randint(1, 100) for _ in range(4))
        self.solution = f"{a * d}/{b * c}"
        self.question_text = f"Calculate: {a}/{b} ÷ {c}/{d}"
        distractor1 = f"{(a * d) + 1}/{b * c}"  # small numerator error
        distractor2 = f"{a * d}/{b + c}"         # wrong denominator operation
        distractor3 = f"{a + b}/{c + d}"          # unrelated operation

        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

    def generate_fraction_conversion(self):
        """
        Generates a fraction-to-decimal conversion question.
        Returns:
            tuple: (question text, solution, distractors)
        """
        denominator = random.randint(1, 1000)
        numerator = random.randint(1, denominator - 1)
        decimal = "0."
        self.question_text = f"Convert this fraction to a decimal: {numerator}/{denominator}"
        num = numerator * 10

        while True:
            while num < denominator:
                decimal += "0"
                num *= 10

            decimal += str(num // denominator)
            num %= denominator

            if num == 0 or len(decimal) > 13:
                break

            num *= 10

        self.solution = decimal

        # Generate slight variations as distractors
        if decimal[-1].isdigit():
            last_digit = int(decimal[-1])
            new_digit = (last_digit + 1) % 10
            distractor1 = decimal[:-1] + str(new_digit)
        else:
            distractor1 = decimal

        distractor2 = decimal[:-1] if len(decimal) > 3 else decimal
        distractor3 = decimal + str(random.randint(0, 9))

        self.distractors = [distractor1, distractor2, distractor3]
        return self.question_text, self.solution, self.distractors

# Example usage:
if __name__ == "__main__":
    fqg = FractionQG()
    question_data = fqg.generate()
    print("Question Type:", question_data["type"])
    print("Question:", question_data["question"])
    print("Solution:", question_data["solution"])
    print("Distractors:", question_data["distractors"])
