# DO NOT MODIFY THIS FILE.
#
# Any modifications to this file will not be used when grading your project.
# If you have any questions, please email the TAs.
#
# The main driver file for the project. You may edit this file to change which
# problems your Agent addresses while debugging and designing, but you should
# not depend on changes to this file for final execution of your project. Your
# project will be graded using our own version of this file.

import os
import sys
import csv
import time

from Agent import Agent
from ProblemSet import ProblemSet
from RavensGrader import grade


def getNextLine(r):
    return r.readline().rstrip()

# The project's main solve method. This will generate your agent's answers
# to all the current problems.
#
# You do not need to use this method.


def solve():
    sets = []  # The variable 'sets' stores multiple problem sets.
    # Each problem set comes from a different folder in /Problems/
    # Additional sets of problems will be used when grading projects.
    # You may also write your own problems.

    # ProblemSetList.txt lists the sets to solve.
    r = open(os.path.join("Problems", "ProblemSetList.txt"))
    # Sets will be solved in the order they appear in the file.
    line = getNextLine(r)
    # You may modify ProblemSetList.txt for design and debugging.
    while not line == "":
        # We will use a fresh copy of all problem sets when grading.
        sets.append(ProblemSet(line))
        # We will also use some problem sets not given in advance.
        line = getNextLine(r)

    # Initializing problem-solving agent from Agent.java
    # Your agent will be initialized with its default constructor.
    agent = Agent()
    # You may modify the default constructor in Agent.java

    # Running agent against each problem set
    # Results will be written to ProblemResults.csv.
    with open("AgentAnswers.csv", "w") as results:
        # Note that each run of the program will overwrite the previous results.
        # Do not write anything else to ProblemResults.txt during execution of the program.
        results.write("ProblemSet,RavensProblem,Agent's Answer\n")
        for set in sets:
            for problem in set.problems:   # Your agent will solve one problem at a time.
                # try:
                # The problem will be passed to your agent as a RavensProblem object as a parameter to the Solve method
                answer = agent.Solve(problem)
                # Your agent should return its answer at the conclusion of the execution of Solve.

                results.write("%s,%s,%d\n" % (set.name, problem.name, answer))
    r.close()

# The main execution will have your agent generate answers for all the problems,
# then generate the grades for them.


def main():
    start = time.time()
    solve()
    end = time.time()
    grade()


if __name__ == "__main__":
    main()
