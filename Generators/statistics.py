import random
from Generators.distractors_generator import DistractorsGenerator

class Statistics(DistractorsGenerator):
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["mean_median_mode"])

        if self.question_type == "mean_median_mode":
            self.mean_median_mode()

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

        