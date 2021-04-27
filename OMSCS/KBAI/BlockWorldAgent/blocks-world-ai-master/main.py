"""
Created on Apr 4, 2019

@author: Apostolis Tselios
"""
import os
import utils
import time
import sys
from tree_node import TreeNode


def search(queue, method, initial, goal):
    """Searches the tree for a solution based on the search algorithm."""
    root = TreeNode(initial, None, None, 0, 0, 0)

    if method == 'astar' or method == 'best':
        # If the method uses a heuristic a PriorityQueue is initialized with the root.
        queue.put((0, root))
    else:
        queue.put(root)

    visited_set = set()  # Set of visited states.
    start = time.time()
    while (not queue.empty()) and (time.time() - start <= 60):
        # While the queue is not empty and a minutes hasn't passed.

        if method == 'astar' or method == 'best':
            # PriorityQueue .get() method returns the priority number and the element.
            curr_f, current = queue.get()
        else:
            current = queue.get()

        if current.is_goal(goal):
            return current

        if str(current.state) in visited_set:
            # If this state has been visited before don't add it to the children
            # and continue with the next child.
            continue

        current.find_children(method, goal)
        visited_set.add(str(current.state))  # Mark the state as visited.

        # Add every child in the search queue.
        for child in current.children:
            if method == 'depth' or method == 'breadth':
                queue.put(child)
            elif method == 'astar' or method == 'best':
                queue.put((child.f, child))

    return None


def main():
    start = time.time()  # Start time.
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears the terminal.

    # Handles the arguments.
    if len(sys.argv) == 3:
        # If the args are 3 no output file name wasn't specified.
        method = sys.argv[1]
        input_file = sys.argv[2]
    elif len(sys.argv) == 4:
        # If the args are 4 the output file name was specified.
        method = sys.argv[1]
        input_file = sys.argv[2]
        output_file = sys.argv[3]
    else:
        print(
            f'Usage: {sys.argv[0]} <search algorithm> <problem file name> <solution file name>')
        print('- search algorithms: depth (Depth First), breadth (Breadth First), best (Best First), astar (A*)')
        sys.exit()

    # Initializes the type of queue based on the search method.
    search_queue = utils.METHODS[method]

    # Parse the data and get the objects (blocks), initial state and the goal state.
    data = utils.load_problem(input_file)
    objects = utils.get_objects_from_file(data)
    initial_state = utils.get_initial_state(data)
    goal_state = utils.get_goal_state(data)

    print('OBJECTS:', objects)

    print('\n#################### INITIAL STATE ####################\n')
    print(initial_state)
    i_blocks = utils.initialize_blocks(objects, initial_state)

    print('\n#################### GOAL STATE ####################\n')
    print(goal_state)
    g_blocks = utils.initialize_blocks(objects, goal_state)

    solution_node = search(search_queue, method, i_blocks, g_blocks)

    if solution_node != None:
        # If a solution is found.
        print('\n#################### SOLUTION ####################\n')
        solution_node.print_state()
        print(f'Number of moves: {solution_node.g}')

        # Calculates the time it took to find the solution.
        print('Took: ', time.time() - start)

        solution_path = solution_node.get_moves_to_solution()

        if len(sys.argv) == 3:
            # If the output file name was not specified.
            try:
                # Handling the paths with forward-slashes and back-slashes.
                file_name = input_file.split('\\')[-1]
                output_file = './solutions/' + method + '-' + file_name
                utils.write_solution(output_file, solution_path)
            except FileNotFoundError:
                file_name = input_file.split('/')[-1]
                output_file = './solutions/' + method + '-' + file_name
                utils.write_solution(output_file, solution_path)
        else:
            # If the output file name is specified.
            utils.write_solution(output_file, solution_path)
    else:
        print('Took: ', time.time() - start)
        print('############ ONE MINUTE PASSED AND NO SOLUTION WAS FOUND ############')
        sys.exit()


if __name__ == '__main__':
    main()
