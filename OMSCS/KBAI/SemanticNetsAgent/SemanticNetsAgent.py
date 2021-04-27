from collections import deque
import time


class SemanticNetsAgent:
    def __init__(self):
        # List of all states that have been visited
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
        self.initial_s = 0
        self.initial_w = 0

    def solve(self, initial_sheep, initial_wolves):
        current_state = State(0, initial_sheep, 0, initial_wolves, 0)
        self.initial_s = initial_sheep
        self.initial_w = initial_wolves
        return self.check(current_state)

    def check(self, state):
        start_time = time.time()
        self.states.append((state, (0, 0)))
        self.visited.add(state.returnAsTuple())
        while self.states:
            next_state = self.states.popleft()
            # print(next_state[1])
            for i in self.possible_moves:
                # Generated the state after applying the move
                generated_state = next_state[0].applyMove(
                    i, next_state[0].ship_current)
                if generated_state:
                    # Check if the generated state is in the state history
                    if generated_state.returnAsTuple() not in self.visited:
                        self.parents[(generated_state.returnAsTuple(), i)
                                     ] = next_state[0].returnAsTuple()
                        self.visited.add(generated_state.returnAsTuple())
                        self.states.append((generated_state, i))

                    # Check if the generated state is the solution
                    if next_state[0].sheep_r == self.initial_s and next_state[0].wolf_r == self.initial_w:
                        self.visited.add(generated_state.returnAsTuple())
                        self.states.append((generated_state, i))
                        start = (0, self.initial_s, 0, self.initial_w, 0)
                        to_return = []
                        state = next_state[0].returnAsTuple()

                        while state != start:
                            for key in self.parents:
                                if key[0] == state:
                                    to_return.append(key[1])
                                    state = self.parents.get(key)
                        elapsed_time = time.time() - start_time
                        elapsed_time = str(elapsed_time)
                        # print('Elapsed Time for' +
                        # str(initial_state) + ' ' + elapsed_time)
                        return elapsed_time
        elapsed_time = time.time() - start_time
        elapsed_time = str(elapsed_time)
        # print('Elapsed Time for' +
        # str(initial_state) + ' ' + elapsed_time)
        return elapsed_time


class State:
    def __init__(self, ship_current, sheep_l, sheep_r, wolf_l, wolf_r):
        self.ship_current = ship_current
        self.sheep_l = sheep_l
        self.sheep_r = sheep_r
        self.wolf_l = wolf_l
        self.wolf_r = wolf_r

    def returnAsTuple(self):
        return (self.ship_current, self.sheep_l, self.sheep_r, self.wolf_l, self.wolf_r)

    def applyMove(self, move, counter):
        s_move = move[0]
        w_move = move[1]

        if counter % 2 == 0:  # even, ship on the left.
            if self.sheep_l < s_move or self.wolf_l < w_move:
                return None
            new1 = self.sheep_l - s_move
            new2 = self.sheep_r + s_move
            new3 = self.wolf_l - w_move
            new4 = self.wolf_r + w_move
        else:
            if self.sheep_r < s_move or self.wolf_r < w_move:
                return None
            new1 = self.sheep_l + s_move
            new2 = self.sheep_r - s_move
            new3 = self.wolf_l + w_move
            new4 = self.wolf_r - w_move

        # Check if wolf is more than sheep and for any negatives
        if (new4 > new2 and new2 != 0) or (new3 > new1 and new1 != 0):
            return None

        if counter % 2 == 0:
            ship_current = 1  # If previously even, ship is now on the right
        else:
            ship_current = 0  # If previously odd, ship is now on the left

        new_state = State(ship_current, new1,
                          new2, new3, new4)

        return new_state
