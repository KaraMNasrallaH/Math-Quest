import random
from Generators.distractors_generator import DistractorsGenerator

class AlgebraBasicQG(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["whatx", "exponents_laws", "polynomial"])
        if self.question_type == "whatx":
            self.what_is_x()
        elif self.question_type == "exponents_laws":
            self.exponents_laws()
        elif self.question_type == "polynomial":
            self.polynomial()
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
    
    def polynomial(self):
        self.distractors = []

        def generate_terms(degree, groups):
            terms = {}
            degree += 1
            for i in range(degree):
                exp = degree - 1 - i
                coeffs = [random.randint(-5, 10) for _ in range(groups)]
                terms[exp] = coeffs
            return terms

        def format_terms(terms, degree, operator=""):
            formatted = {}
            for exp in terms.keys():
                var = "x^"
                coeffs = terms[exp]
                formatted[exp] = []
                exp_val = exp

                if exp_val == 1:
                    exp_val, var = "", "x"
                elif exp_val == 0:
                    exp_val, var = "", ""

                if isinstance(coeffs, int):
                    coeffs = [coeffs]

                for c in coeffs:
                    coefficient = abs(c)
                    sign = ' + ' if c >= 0 else ' - '
                    if c >= 0 and exp == degree:
                        sign = ""
                    if c == 0:
                        formatted[exp].append("")
                        continue
                    elif c == 1 and exp > 0:
                        coefficient = ""
                    formatted[exp].append(f"{sign}{coefficient}{var}{exp_val}")

            grouped_terms = list(zip(*(formatted[exp] for exp in formatted)))
            if len(grouped_terms) == 1:
                return "".join(grouped_terms[0])
            parts = [f"({' '.join(g).strip()})" for g in grouped_terms]
            return f" {operator} ".join(parts)

        def solve_terms(terms, operator=""):
            total = {}
            if operator == '*' or "":
                n_groups = len(next(iter(terms.values())))
                group_dicts = []
                for i in range(n_groups):
                    grp = {exp: coeffs[i] for exp, coeffs in terms.items()}
                    group_dicts.append(grp)
                total = {0: 1}
                for grp in group_dicts:
                    new_total = {}
                    for exp1, coef1 in total.items():
                        for exp2, coef2 in grp.items():
                            exp_sum = exp1 + exp2
                            prod = coef1 * coef2
                            new_total[exp_sum] = new_total.get(exp_sum, 0) + prod
                    total = new_total
            else:
                if operator == '+':
                    total = {exp: sum(coeffs) for exp, coeffs in terms.items()}
                else:
                    total = {}
                    for exp, coeffs in terms.items():
                        first, *rest = coeffs
                        total[exp] = first - sum(rest)
            return total

        operator = random.choice(["+", "-", "*"])
        degree = 1 if operator in ["*",""] else 2
        groups = 2
        terms = generate_terms(degree, groups)

        self.question_text = format_terms(terms, degree, operator)
        result = solve_terms(terms, operator)
        self.solution = format_terms(result, degree)

        seen = {self.solution}
        MAX_ATTEMPTS = 20
        for _ in range(3):
            attempts = 0
            while attempts < MAX_ATTEMPTS:
                fake = result.copy()
                non_zero_exps = [e for e, c in result.items() if c != 0]
                if not non_zero_exps:
                    non_zero_exps = list(result.keys())
                exp = random.choice(non_zero_exps)

                def noisy(true):
                    while True:
                        n = random.choice([-1, 1]) * random.randint(1, 6)
                        val = true + n
                        if val != 0:
                            return val

                fake[exp] = noisy(result[exp])
                candidate = format_terms(fake, degree)

                if candidate not in seen and candidate.strip():
                    seen.add(candidate)
                    self.distractors.append(candidate)
                    break
                attempts += 1

            if attempts >= MAX_ATTEMPTS:
                self.distractors.append("0")

        
        
        
        

            
            
                

            


            










        

