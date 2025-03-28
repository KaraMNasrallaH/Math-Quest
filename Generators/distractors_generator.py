import random

class DistractorsGenerator:
    def distractors_generator(self, result, title=False):
        possible_offsets = list(range(1, 6))
        unique_offsets = random.sample(possible_offsets, 3)
        if title:
            return [f"{title}: {result + offset}" for offset in unique_offsets]
        else:
            return [
                str(round(result + offset, 2)) if isinstance(result, float) else str(result + offset)
                for offset in unique_offsets
            ]
