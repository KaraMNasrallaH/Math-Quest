import random

class DistractorsGenerator:
    def distractors_generator(self, result, value=3, title=False):
        offsets = random.sample(range(1, 6), value)
        sign = 1 if random.choice(["+", "-"]) == "+" else -1
        
        distractors = [result + sign * offset for offset in offsets]
        
        if isinstance(result, float):
            distractors = [round(val, 2) for val in distractors]

        if title:
            return [f"{title}: {val}" for val in distractors]
        else:
            return [str(val) for val in distractors]
