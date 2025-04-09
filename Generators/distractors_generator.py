import random  # Import random module for generating random numbers

class DistractorsGenerator:
    def distractors_generator(self, result, value=3, title=False, rounding=2):
        # Generate unique random offsets between 1 and 5
        offsets = random.sample(range(1, 6), value)

        # Randomly choose whether to add or subtract the offsets
        sign = 1 if random.choice(["+", "-"]) == "+" else -1
        
        # Apply the offsets to create distractors
        distractors = [result + sign * offset for offset in offsets]
        
        # Round values if the result is a float
        if isinstance(result, float):
            distractors = [round(val, rounding) for val in distractors]

        # Format distractors with title if provided
        return [f"{title}: {val}" for val in distractors] if title else [str(val) for val in distractors]

