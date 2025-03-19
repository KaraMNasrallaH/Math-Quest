import random

class RatiosANDProportionQG:
    def __init__(self):
        self.question_text = None
        self.solution = None
        self.distractors = []
        self.question_type = None
    
    def generate(self):
        self.question_type = random.choice(["ratio","ratio_part","percent_ratio"])
        
        if self.question_type == "ratio":
            self.ratio()
        elif self.question_type == "ratio_part":
            self.ratio_part()
        elif self.question_type == "percent_ratio":
            self.percent_ratio()
            

        return {
            "question": self.question_text,
            "solution": self.solution,
            "distractors": self.distractors
        }
    
    def ratio_generator(self,multiplier=False):
        ratio_A = random.randint(2, 20)
        ratio_B = random.randint(2, 30)
        if multiplier:
            multiplier = random.randint(2,20)
            return ratio_A, ratio_B, multiplier
        return ratio_A, ratio_B

    def ratio(self):
        ratio_A, ratio_B, multiplier = self.ratio_generator(multiplier=True)

        total_parts = ratio_A + ratio_B
        total = total_parts * multiplier
        
        self.question_text = (f"The ratio of red to blue marbles is {ratio_A}:{ratio_B}.\n"
                              f"If total marbles is {total}, how many red and blue marbles are there?")
        
        result = total // total_parts
        correct_red = result * ratio_A
        correct_blue = result * ratio_B
        self.solution = f"Red: {correct_red}, Blue: {correct_blue}"
        self.distractors = [
            f"Red: {result * ratio_B}, Blue: {result * ratio_A}",
            f"Red: {result * (ratio_A + 1)}, Blue: {result * (ratio_B - 1)}",
            f"Red: {round(total / ratio_A)}, Blue: {round(total / ratio_B)}"
        ]
    
    def ratio_part(self):
        ratio_A, ratio_B, multiplier = self.ratio_generator(multiplier=True)

        total_parts = ratio_A + ratio_B
        total = total_parts * multiplier
        result = total // total_parts
        correct_A = result * ratio_A
        correct_B = result * ratio_B

        if random.random() > 0.5:
            self.question_text = (f"In a basket, the ratio of apples to oranges is {ratio_A}:{ratio_B}\n"
                                  f"If there are {correct_A} apples, how many oranges are there?")
        else:
            self.question_text = (f"The ratio of boys to girls in a class is {ratio_A}:{ratio_B}\n"
                                  f"If there are {correct_A} boys, how many girls are there?")
            
        self.solution = f"{correct_B}"
        self.distractors = [str(correct_B + random.randint(0,5)) for _ in range(3)]
        
    def percent_ratio(self):
        ratio_A, ratio_B, multiplier = self.ratio_generator(multiplier=True)
        percent_A, percent_B = self.ratio_generator()

        new_ratio_A = (ratio_A * (100 + percent_A)) / 100
        new_ratio_B = (ratio_B * (100 - percent_B)) / 100
        total_parts = new_ratio_A + new_ratio_B
        total = round(total_parts * multiplier,2)
        correct_A = round(ratio_A * (total/total_parts),2)
        correct_B = round(ratio_B  * (total/total_parts),2)
        if correct_A.is_integer():
            correct_A = int(correct_A)  
        if correct_B.is_integer():
            correct_B = int(correct_B)
        
        self.question_text = (
            f"Ingredients are in a {ratio_A}:{ratio_B} ratio. If ingredient A increases by {percent_A}% and ingredient B"
            f"\ndecreases by {percent_B}%, the total becomes {total} cups. Determine the original amounts"
        )
        self.solution = f"{correct_A},{correct_B}"
        self.distractors = [
            f"{correct_A + random.randint(0, 6)},{correct_B + random.randint(1, 6)}"
            for _ in range(3)
        ]



if __name__ == "__main__":
    test = RatiosANDProportionQG()
    question_data = test.generate()
    print(question_data["question"])
    print(question_data["solution"])
    print(question_data["distractors"])