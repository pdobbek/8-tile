"""
- keeps track of each visited node. (closed list)
- has a list of all the nodes that are left to be explored. (open list)
- initially, the open list holds the root node.
- the next node chosen from the open list  is based on its f score (node
lowest f score is picked).
- f_score = h_score - g_score
- h_score: how far the goal node is. In 8-puzzle this can be defined as
number of misplaced tiles.
- g_score: the number of nodes traversed from root node to this node.

How to solve 8-puzzle with A*:
- move the 0 in all possible directions.
- calculate the f_score for each state.
- push root into closed_list and all the new states into open_list.
- select state in open_list with lowest f_score and repeat.
"""


class Puzzle:
    goal_state = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]

    def __init__(self, root):
        self.closed_list = [root]
        self.opened_list = []
