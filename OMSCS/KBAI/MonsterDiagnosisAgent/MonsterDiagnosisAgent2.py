from itertools import combinations
from collections import defaultdict


class MonsterDiagnosisAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, diseases, patient):
        if patient is not None:
            raise Exception(f"Diseases:\n{diseases}\n patient:\n{patient}")
