# Blocks World AI

A basic AI that solves the Blocks World Problem using searching algorithms.
Built in Python 3.7.

### Searching algorithms

* Depth First Search (DFS)
* Breadth First Search (BFS)
* Best First Search
* A*

### Heuristic

Algorithms like Best First Search and A* need a heuristic function to rate
states.

The heuristic function checks if every block is in the correct position,
if not adds 1 to the heuristic value of that state. Furthermore it checks
if the block directly under every block is in the correct position, if not
adds 1 to the heuristic value of that state.

A* and Best First chose the state with the smallest heuristic value.

### Running the program

The program takes 3 command line arguments:

* Search algorithm: depth/breadth/best/astar
* Problem file name: Choose a .txt file from the problems folder.
* Solution file name: Optional. If it's not specified the solution will be
    saved in a folder called solutions.

To run it simply type in your terminal the following command:
```
python main.py depth ./problems/probBLOCKS-4-0.txt
```
