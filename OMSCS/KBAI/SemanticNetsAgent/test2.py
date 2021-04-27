from collections import deque
import time


class SemanticNetsAgent:
    def __init__(self):
        self.visited = set()
        # List of moves to be returned
        self.return_moves = []
        # List of all possible moves
        self.possible_moves = [
            (1, 0),  # One Sheep Moves
            (2, 0),  # Two Sheep Moves
            (0, 1),  # One WolfG Moves
            (0, 2),
            (1, 1)
        ]
        self.counter = 0
        self.states = deque()
        self.parents = {}  # Store the state and the parent.
        self.initials = 0
        self.initialw = 0

    def solve(self, initial_sheep, initial_wolves):
        to_return = []
        return to_return
