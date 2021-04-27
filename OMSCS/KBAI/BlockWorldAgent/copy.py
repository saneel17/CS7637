import heapq


class PriorityQueue:
    def __init__(self):
        self._data = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._data, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._data)[-1]

    def size(self):
        return len(self._data)


class BlockWorldAgent:
    def __init__(self):
        self.queue = PriorityQueue()
        self.visited = set()
        self.parents = {}

    def solve(self, initial_arrangement, goal_arrangement):
        # Converting the lists into a dictionary
        current_dict = self.convert_to_state(initial_arrangement)
        goal_dict = self.convert_to_state(goal_arrangement)

        # Adding the first state into the priority queue, with a score of 0.
        self.queue.push((current_dict, 0), 0)

        # Convert the firs state into a tuple and store it into a set called visited.
        self.visited.add(self.return_as_tuple(current_dict))

        while self.queue:  # While queue is not empty
            # Get the state with the highest score from the Priority Queue
            next_state = self.queue.pop()
            children = self.possible_moves(next_state[0])
            for i in children:
                # print(i[0])
                print(i[1])
                if self.return_as_tuple(i[0]) not in self.visited:
                    self.visited.add(self.return_as_tuple(i[0]))
                    self.parents[self.return_as_tuple(
                        i[0])] = self.return_as_tuple(next_state[0])

                    score = self.heuristic(i[0], goal_dict)
                    self.queue.push(i, score)

                    if self.return_as_tuple(next_state[0]) == self.return_as_tuple(goal_dict):
                        self.visited.add(self.return_as_tuple(i[0]))
                        self.queue.push(i, score)
                        to_return = []
                        state = self.return_as_tuple(next_state[0])

                        while state != self.return_as_tuple(current_dict):
                            for key in self.parents:
                                if key[0] == state:
                                    to_return.append(key[1])
                                    state = self.parents.get(key)
                        return to_return

    def heuristic(self, current, goal):
        '''heuristic to track the difference between the states and goal state
        For each block, track whether it is in the correct goal state. Also, check whether it is at least above/below the intended
        state.
        '''
        score = 0
        for i in current:
            if not current[i] == goal[i]:
                score += 1

            if not current[i]['on_table']:
                on = current[i]['on_top_of']
                if current[on] != goal[on]:
                    score += 1

        return score

    def possible_moves(self, state):
        '''returns a list of moves
        There are 3 moves that a CLEAR block can perform
        1) CLEAR to CLEAR - From a clear block to on top of another block
        2) CLEAR to TABLE - From a clear block to the table
        3) TABLE to CLEAR - From the table to on top of another block
        '''
        blocks = {key: value for key,
                  value in state.items() if value['clear']}

        moves = []
        for block, value in blocks.items():
            # For every clear block that is on top of another block,
            if value['on_top_of'] != -1:
                on = value['on_top_of']
                temp_state = self.clear_to_table(state, block, on)
                moves.append(temp_state)

                for i in blocks:
                    if i != block:
                        # Move a clear Block on a clear Block.
                        temp_state = self.clear_to_clear(state, block, i)
                        moves.append(temp_state)

            elif value['on_table']:
                # Move a Block on table on a clear Block.
                for i in blocks:
                    if i != block:
                        temp_state = self.table_to_clear(state, block, i)
                        moves.append(temp_state)

        del blocks
        return moves

    def table_to_clear(self, state, block, on):
        '''
        Method to move a clear block on a table to another clear block
        '''
        copy = {key: state[key].copy() for key in state}
        copy[block]['on_table'] = False
        copy[block]['on_top_of'] = on
        copy[on]['clear'] = False
        copy[on]['below_of'] = block
        move = (block, on)

        return copy, move

    def clear_to_table(self, state, block, on):
        '''
        Method to move a clear block to table.
        '''
        copy = {key: state[key].copy() for key in state}

        copy[block]['on_table'] = True
        copy[block]['on_top_of'] = -1
        copy[on]['clear'] = True
        copy[on]['below_of'] = -1
        move = (block, 'table')

        return copy, move

    def clear_to_clear(self, state, block, on):
        copy = {key: state[key].copy() for key in state}

        copy[block]['on_table'] = False
        copy[block]['on_top_of'] = on
        copy[on]['clear'] = False
        copy[on]['below_of'] = block
        move = (block, on)

        return copy, move

    def convert_to_state(self, this_list):
        '''Returns a Dictionary of the Current State in Block World
        Each Block is a key, and has a Dictionary of
        a) Clear (Boolean) - The block does not have anything on top of it. It can either be on a table or
        it can be on top of another block. It can be moved.
        b) On_Table (Boolean) - The block is on the table.
        c) On_Top_Of - What block this block is on top off. If it is not on top of anything, return -1.
        d) Below_Of - What block this block is below of. If it is not below anything, return -1.
        '''
        this_dict = {}
        for i in this_list:
            # Get length of the list
            length = len(i)
            if length == 0:  # If there is only one block on the table.
                this_dict[i[0]] = {'clear': True, 'on_table': True,
                                   'on_top_of': -1, 'below_of': -1}
            else:  # If there is more than one block on the table
                for j in range(length):
                    # If first block
                    if j == 0:
                        above = i[j + 1]
                        this_dict[i[j]] = {'clear': False, 'on_table': True,
                                           'on_top_of': -1, 'below_of': above}
                    # If Last block,
                    elif j == length - 1:
                        below = i[j - 1]
                        this_dict[i[j]] = {'clear': True, 'on_table': False,
                                           'on_top_of': below, 'below_of': -1}
                    else:
                        above = i[j + 1]
                        below = i[j - 1]
                        this_dict[i[j]] = {'clear': False, 'on_table': False,
                                           'on_top_of': below, 'below_of': above}
        return this_dict

    def return_as_tuple(self, state):
        this_list = []
        x = sorted(state.items())
        for i in x:
            y = tuple(i[1].items())
            z = (i[0], y)
            this_list.append(z)
        return tuple(this_list)
