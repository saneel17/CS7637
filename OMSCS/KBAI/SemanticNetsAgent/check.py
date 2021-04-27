from collections import deque


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
        self.initials = 0
        self.initialw = 0

    def solve(self, initial_sheep, initial_wolves):
        current_state = State(0, initial_sheep, 0, initial_wolves, 0)
        self.initials = initial_sheep
        self.initialw = initial_wolves
        return self.check(current_state)

    def check(self, state):
        self.states.append((state, (0, 0)))
        self.visited.add(state.returnAsTuple())
        while self.states:
            next_state = self.states.popleft()
            print("Popped State:" + str(next_state[0].returnAsTuple()))

            # print(next_state[1])
            for i in self.possible_moves:
                # Generated the state after applying the move
                generated_state = next_state[0].applyMove(
                    i, next_state[0].ship_current)
                if generated_state:
                    # Check if the generated state is the solution
                    # Check if the generated state is in the state history
                    if generated_state.returnAsTuple() not in self.visited:
                        self.parents[(generated_state.returnAsTuple(), i)
                                     ] = next_state[0].returnAsTuple()
                        self.visited.add(generated_state.returnAsTuple())
                        self.states.append((generated_state, i))
                        print("Generated States:" +
                              str(generated_state.returnAsTuple()))

                    if next_state[0].sheep_r == self.initials and next_state[0].wolf_r == self.initialw:
                        self.visited.add(generated_state.returnAsTuple())
                        self.states.append((generated_state, i))
                        start = (0, self.initials, 0, self.initialw, 0)
                        to_return = []
                        state = next_state[0].returnAsTuple()

                        while state != start:
                            print(state)
                            to_return.append(list(self.parents.keys())[
                                list(self.parents.values()).index(state)][1])
                            state = list(self.parents.keys())[
                                list(self.parents.values()).index(state)][0]
                            return to_return

            return self.parents


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
        all_list = [new1, new2, new3, new4]
        if (new4 > new2 and new2 != 0) or (new3 > new1 and new1 != 0):
            return None

        if counter % 2 == 0:
            ship_current = 1  # If previously even, ship is now on the right
        else:
            ship_current = 0  # If previously odd, ship is now on the left

        new_state = State(ship_current, new1,
                          new2, new3, new4)

        return new_state
