import copy


class TreeNode(object):
    """ Implementation of a TreeNode used in the search algorithms."""

    def __init__(self, state, parent, move, h, g, f):
        self.state = state
        self.parent = parent
        self.move = move
        self.h = h
        self.g = g
        self.f = f
        self.children = []

    def find_children(self, method, goal):
        """ Finds the children of a TreeNode object. If the child has been
        already visited is not added to the object's children list."""

        moves = self.find_possible_moves()
        for state in moves:
            g = self.g + 1
            if method == 'astar':
                h = self.heuristic(state[0], goal)
                f = h + g
                self.children.append(
                    TreeNode(state[0], self, state[1], h=h, g=g, f=f))
            elif method == 'best':
                h = self.heuristic(state[0], goal)
                self.children.append(
                    TreeNode(state[0], self, state[1], h=h, g=g, f=h))
            else:
                self.children.append(
                    TreeNode(state[0], self, state[1], h=0, g=g, f=0))

    def find_possible_moves(self):
        """Finds and returns the possible moves in the current state."""

        # Initialize a dictionary with the clear blocks.
        clear_blocks = {key: value for key,
                        value in self.state.items() if value['CLEAR']}

        moves = []
        for block, value in clear_blocks.items():
            # For every clear block.
            if value['ON'] != -1:
                # Move a clear Block on table.
                on = value['ON']
                temp_state = self.clear_on_table(block, on)
                moves.append(temp_state)

                for block_ in clear_blocks:
                    if block != block_:
                        # Move a clear Block on a clear Block.
                        temp_state = self.clear_on_clear(block, block_)
                        moves.append(temp_state)

            elif value['ONTABLE']:
                # Move a Block on table on a clear Block.
                for block_ in clear_blocks:
                    if block != block_:
                        temp_state = self.table_on_clear(block, block_)
                        moves.append(temp_state)

        del clear_blocks
        return moves

    def clear_on_table(self, block, on):
        """ Move a clear block that is on another block on table. """

        # A copy of the current state.
        copy_blocks = {key: self.state[key].copy() for key in self.state}

        copy_blocks[block]['ONTABLE'] = True
        copy_blocks[block]['ON'] = -1
        copy_blocks[on]['CLEAR'] = True
        copy_blocks[on]['UNDER'] = -1
        move = (block, on, 'table')

        return copy_blocks, move

    def table_on_clear(self, block, block_):
        """Moves a block that is on table on a clear block."""

        # A copy of the current state.
        copy_blocks = {key: self.state[key].copy() for key in self.state}

        copy_blocks[block]['ONTABLE'] = False
        copy_blocks[block]['ON'] = block_
        copy_blocks[block_]['UNDER'] = block
        copy_blocks[block_]['CLEAR'] = False
        move = (block, 'table', block_)

        return copy_blocks, move

    def clear_on_clear(self, block, block_):
        """Moves a clear block that is on a block on another clear block."""

        # A copy of the current state.
        copy_blocks = {key: self.state[key].copy() for key in self.state}

        below_block = copy_blocks[block]['ON']

        copy_blocks[block]['ON'] = block_
        copy_blocks[below_block]['CLEAR'] = True
        copy_blocks[below_block]['UNDER'] = -1
        copy_blocks[block_]['UNDER'] = block
        copy_blocks[block_]['CLEAR'] = False
        move = (block, below_block, block_)

        return copy_blocks, move

    def heuristic(self, state, goal):
        """Score the nodes checking every block if it's in the correct position and if
        the block under it is in the correct position. (if it has a block under it.)"""

        score = 0
        for block in state:
            if not state[block] == goal[block]:
                # If the block its not in its goal position add 1 to the score.
                score += 1

            if not state[block]['ONTABLE']:
                # If the block is not on table check if the block that is on is in the correct position.
                on = state[block]['ON']
                if state[on] != goal[on]:
                    # If its not add 1 to the score.
                    score += 1

        return score

    def print_state(self):
        """Prints the current state."""
        for block, value in self.state.items():
            print(f'{block}:{value}')

    def is_goal(self, goal):
        """Checks if the currents state is equal to the goal."""
        return self.state == goal

    def get_moves_to_solution(self):
        """Returns a list with the moves you have to make in order to reach the solution."""

        temp_node = copy.copy(self)
        path = []
        while temp_node.parent is not None:
            if temp_node.move is not None:
                path.append(temp_node.move)
            temp_node = temp_node.parent

        return path

    def __lt__(self, other):
        """ Larger than operation of TreeNode object. """
        return self.f < other.f

    def __eq__(self, other):
        """ Equal operation on TreeNode object. """
        if other is not None:
            return self.state == other.state


if __name__ == '__main__':
    pass
