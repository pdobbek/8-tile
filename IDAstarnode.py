import copy
import time
from sortedcontainers import SortedList
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
- set depth to 0.
- move the 0 in all possible directions.
- calculate the f_score for each state.
- push root into closed_list and all the new states into open_list.
- set depth to the lowest f_score in the open_list.
- select state in open_list with lowest f_score and repeat.
"""

goal_state = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]
open_list = SortedList()
closed_list = []
move_counter = 0


class Node:

    def __init__(self, state, g=0):
        self.state = state
        self.h = self.calculate_h()
        self.g = g
        self.f = self.h - g

    @property
    def blank_pos(self):
        return self.state[0], self.state[1]

    @property
    def grid(self):
        return self.state[2]

    @property
    def is_goal(self):
        return self.h == 0

    def calculate_h(self) -> int:
        h = 0
        n = len(self.grid)
        for i in range(n):  # for each row in state
            for j in range(n):  # for each number in row
                if self.grid[i][j] != goal_state[2][i][j]:
                    h += 1  # if not the same as goal state
        return h

    def generate_children(self):
        for child in self.move():
            if child not in closed_list and child not in open_list:
                open_list.add(child)

    def move(self):  # node
        """
        Generator which yields a new state for each possible move after moving
        the blank tile with move_blank function.
        Doesn't change the arg state.
        Increment the move_counter global variable each time it's called.
        :param state: list
            state to base the yielded states on.
        :return:
            new Node with state after blank tile move.
        """
        global move_counter
        move_counter += 1
        [i, j, grid] = self.state
        n = len(grid)
        for pos in move_blank(i, j, n):
            i1, j1 = pos
            new_grid = copy.deepcopy(grid)
            new_grid[i][j], new_grid[i1][j1] = grid[i1][j1], grid[i][j]  # swap
            yield Node([i1, j1, new_grid], self.g+1)

    def __str__(self):
        return self.state.__str__()

    def __contains__(self, item):
        return self.grid == item.grid

    def __eq__(self, other):
        return self.grid == other.grid

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f


def move_blank(i, j, n):
    """
    Generator which moves the blank tile (prefers order of NSEW).
    :param i: int
        row index of the blank tile.
    :param j: int
        column index of the blank tile.
    :param n: int
        number of rows and columns in the puzzle.
    :return: (int, int)
        tuple of new blank tile row and column index.
    """
    # North
    if i+1 < n:
        yield i + 1, j
    # South
    if i-1 >= 0:
        yield i - 1, j
    # East
    if j+1 < n:
        yield i, j + 1
    # West
    if j-1 >= 0:
        yield i, j - 1


def dfs(root):
    """
    Begins the IDDFS search for solution to the puzzle passed. Solution
    is compared against the goal_state global variable.
    Currently loops indefinitely if the arg puzzle state cannot be
    solved.
    :param root: list
        8-tile puzzle state represented by a list of lists. I.e.
            [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]]
    :return: list
        solution 8-tile puzzle state that is the solution.
    """
    open_list.add(root)
    while True:
        node = open_list.pop(0)
        if node.is_goal:
            return node
        node.generate_children()
        closed_list.append(node)


def solve(puzzle):
    """
    Solves the 8-tile puzzle and prints results to stdout.
    :param puzzle: list
        8-tile puzzle state to be solved.
    :return: list
        list of 8-tile puzzle states that forms the path to the solution.
        Solution is at index [-1]. Initial state is at index [0].
    """
    global move_counter
    move_counter = 0  # reset global var

    start_time = time.time()
    solution = dfs(puzzle)
    end_time = time.time()

    print('-----------------------------------')
    print('initial state:', puzzle)
    print('number of moves:', solution.g)
    print('calls to move:', move_counter)
    print('timer (seconds):', (end_time - start_time))
    print('-----------------------------------')
    return solution


def tests():
    node = Node([2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]], 0)
    test_node = Node([2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]], 0)
    print("__contains ok" if node == test_node else "__contains__ ERROR")
    print("__eq__ ok" if node in [test_node] else "__eq__ ERROR")

    for grid_child in node.move():
        print(grid_child.__str__())
        open_list.add(grid_child)

    print(node > test_node)
    open_list.add(node)
    open_list.add(test_node)
    for element in open_list:
        print(element.f.__str__())


def main():
    global open_list, closed_list, move_counter
    initial_states = [
        [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]],
        [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]],
        [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]],
        [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]],
        [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]],
        [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]],
        [0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]],
        [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]],
        [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]],
        [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]],
        [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]
    ]
    for state in initial_states:
        open_list = SortedList()
        closed_list = []
        solve(Node(state))


if __name__ == '__main__':
    main()
