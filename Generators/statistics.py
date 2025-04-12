import random
from Generators.distractors_generator import DistractorsGenerator

class Statistics(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["mean_median_mode", "probability", "find_range"])

        if self.question_type == "mean_median_mode":
            self.mean_median_mode()
        elif self.question_type == "probability":
            self.probability()
        elif self.question_type == "find_range":
            self.find_range()

        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
        

    
    def mean_median_mode(self):
        a = random.randint(3, 10)
        data_set = sorted([random.randint(1,10) for _ in range(a)])
        self.question_text = f"A student scores the following in {a} tests: {data_set}\nWhat is the mean, median, and mode?"

        # Mean
        mean = round(sum(data_set) / a, 2)

        # Median
        if a % 2 != 0:
            median = data_set[a // 2]
        else:
            first_index = (a // 2) - 1
            second_index = a // 2
            median = (data_set[first_index] + data_set[second_index]) / 2

        # Mode
        repeated = {}
        largest = 0
        mode = []
        for num in data_set:
            if num in repeated:
                repeated[num] += 1
            else:
                repeated[num] = 1

        for key, value in repeated.items():
            if value > 1 and value == largest:
                mode.append(key)
            elif value > 1 and value > largest:
                mode.clear()
                largest = value
                mode.append(key)

        if not mode:
            mode = "No Mode"

        self.solution = f"Mean: {mean}, Median: {median}, Mode: {mode}"
        A_dis = self.distractors_generator(mean, value=2, extra=mean)
        B_dis = self.distractors_generator(median)
        self.distractors = [f"Mean: {a}, Median: {b}, Mode: {mode}" for a, b in zip(A_dis, B_dis)]
    
    def probability(self):
        a, b, c = (random.randint(2, 20) for _ in range(3))
        marbles = {"red": a, "green": b, "yellow": c}
        
        marble_type = random.choice(["red", "green", "yellow"])
        val = marbles[marble_type]
        
        self.question_text = (
            f"In a bag there are 3 types of marbles: {a} red, {b} green, {c} yellow.\n"
            f"What is the probability of getting a {marble_type} marble?"
        )
        
        total = a + b + c
        result = (100 / total) * val
        result = int(result) if result == int(result) else round(result, 2)
        self.solution = f"{result}%"
        A_dis = self.distractors_generator(result)
        self.distractors = [f"{a}%" for a in A_dis]
    
    def find_range(self):
        a = random.randint(3, 10)
        data_set = [random.randint(15,50) for _ in range(a)]
        self.question_text = f"What is the range of this data? {data_set}"
        data_set = sorted(data_set)
        result = data_set[-1] - data_set[0]
        self.solution = f"{result}"
        self.distractors = self.distractors_generator(result)



        




        