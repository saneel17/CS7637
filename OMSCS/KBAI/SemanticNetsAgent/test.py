from SemanticNetsAgent import SemanticNetsAgent
import unittest


class SheepWolvesTests(unittest.TestCase):
    def test(self):
        # This will test your SemanticNetsAgent
        # with seven initial test cases.
        test_agent = SemanticNetsAgent()
        tests = [(1, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (4, 4), (5, 4), (6, 4), (3, 3), (4, 3), (5, 3),
                 (6, 3), (7, 3), (8, 3), (9, 3), (13, 3), (5, 5), (2, 1), (3, 1), (4, 1), (5, 5), (6, 6), (6, 5), (7, 5)]
        test_optimals = [1, 5, 7, 9, 11, 13, 15, 0, 15, 17, 11,
                         11, 13, 15, 17, 19, 21, 29, 0, 3, 5, 7, 0, 0, 19, 21]

        for i in range(len(tests)):
            test = tests[i]
            moves = test_agent.solve(test[0], test[1])
            print('For ', test[0], ',', test[1], ' :', moves)
            left = (test[0], test[1])
            right = (0, 0)
            if len(moves) == 0:
                right = left
            leftSide = True
            for move in moves:
                # print('Move: ',move)
                if leftSide:
                    leftSide = False
                    left = (left[0] - move[0], left[1] - move[1])
                    right = (right[0] + move[0], right[1] + move[1])
                    # print('L:',left,' R:',right)
                else:
                    leftSide = True
                    left = (left[0] + move[0], left[1] + move[1])
                    right = (right[0] - move[0], right[1] - move[1])

            self.assertEqual(right, test, msg="Not a right solution")
            self.assertEqual(
                len(moves), test_optimals[i], msg="Incorrect number of optimal moves")


if __name__ == "__main__":
    unittest.main()
