import copy
import sys
import time

"""
-----------------------------------
initial state: [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]]
number of moves: 16
calls to move: 263
timer (seconds): 0.007998466491699219
-----------------------------------
-----------------------------------
initial state: [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]]
number of moves: 18
calls to move: 1056
timer (seconds): 0.0350649356842041
-----------------------------------
-----------------------------------
initial state: [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]]
number of moves: 20
calls to move: 721
timer (seconds): 0.020375967025756836
-----------------------------------
-----------------------------------
initial state: [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]]
number of moves: 18
calls to move: 1310
timer (seconds): 0.04082608222961426
-----------------------------------
-----------------------------------
initial state: [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]]
number of moves: 18
calls to move: 360
timer (seconds): 0.010000467300415039
-----------------------------------
-----------------------------------
initial state: [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]
number of moves: 18
calls to move: 538
timer (seconds): 0.015775680541992188
-----------------------------------
-----------------------------------
initial state: [0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]]
number of moves: 20
calls to move: 218
timer (seconds): 0.006031990051269531
-----------------------------------
-----------------------------------
initial state: [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]]
number of moves: 14
calls to move: 50
timer (seconds): 0.002758026123046875
-----------------------------------
-----------------------------------
initial state: [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]]
number of moves: 24
calls to move: 3176
timer (seconds): 0.09736037254333496
-----------------------------------
-----------------------------------
initial state: [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]]
number of moves: 22
calls to move: 4265
timer (seconds): 0.09632992744445801
-----------------------------------
-----------------------------------
initial state: [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]
number of moves: 31
calls to move: 43432
timer (seconds): 1.123173475265503
-----------------------------------
"""
"""
Iterative Deepening A* Search program created to solve the 8-tile 
puzzle problem.

This program assumes a pre-set goal state (_goal_state).

Puzzles are in form of lists of lists. I.e.
    [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]
Meaning that the blank tile is in position (2, 1) and the puzzle looks
like so;
    8, 6, 7
    2, 5, 4
    3, 0, 1

@author: Patryk Dobbek, p.dobbek@uea.ac.uk, 100023818
"""

# Global variables
_goal_state = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]
_goal_pos_dict = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }  # dict that matches tile values to their goal-state positions.
_move_counter = 0  # how many calls to Node.move() were performed

class Node:
    """
    Class describing a state of a 8-tile puzzle.
    """

    def __init__(self, state, g=0):
        """
        :param state: list
            list of lists containing the position of the blank state and
            the rows of the puzzle.
        :param g: int
            default=0
            number of moves away from root. When creating a new puzzle,
            parameter should be omitted.
        """
        self.state = state
        self.h = self.__calculate_h()
        self.g = g
        self.f = self.h + g

    @property
    def blank_pos(self) -> (int, int):
        """
        :return: (int, int)
            co-ordinates of the 0 tile (row, column).
        """
        return self.state[0], self.state[1]

    @property
    def grid(self) -> list:
        """
        :return: list
            grid part of the original puzzle array. I.e.
                [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        """
        return self.state[2]

    @property
    def is_goal(self) -> bool:
        """
        :return: bool
            True if this Node is 0 distance away from the goal state.
            False otherwise.
        """
        return self.h == 0

    def __calculate_h(self) -> int:
        """
        This function calculates the approximate distance to the goal
        state by summing the Manhattan distances of all tiles and their
        goal state.
        :return: int
            h - approximate distance to the goal state.
        """
        h = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != 0:
                    goal_pos = _goal_pos_dict[self.grid[i][j]]
                    h += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
        return h

    def move(self):  # ->node
        """
        Generator which yields a new state for each possible move after moving
        the blank tile with _move_blank function.
        Doesn't change this state.
        Increment the move_counter global variable each time it's called.
        :return:
            new Node with state after blank tile move.
        """
        global _move_counter
        [i, j, grid] = self.state
        for pos in self._move_blank():
            _move_counter += 1
            i1, j1 = pos
            new_grid = copy.deepcopy(grid)
            new_grid[i][j], new_grid[i1][j1] = grid[i1][j1], grid[i][j]  # swap
            yield Node([i1, j1, new_grid], self.g+1)

    def _move_blank(self) -> (int, int):
        """
        Generator which moves the blank tile (prefers order of NSEW).
        :return: (int, int)
            tuple of new blank tile row and column index.
        """
        i, j = self.blank_pos
        n = len(self.grid)
        # North
        if i + 1 < n:
            yield i + 1, j
        # South
        if i - 1 >= 0:
            yield i - 1, j
        # East
        if j + 1 < n:
            yield i, j + 1
        # West
        if j - 1 >= 0:
            yield i, j - 1

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


def _ida_star(root) -> list:
    """
    Begins the IDA* search for solution to the puzzle passed. Solution
    is compared against the goal_state global variable.
    Currently loops indefinitely if the arg puzzle state cannot be
    solved.
    :param root: list
        8-tile puzzle state represented by a list of lists. I.e.
            [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]]
    :return: list
        list of Nodes that make up the path to the solution.
    """
    depth = root.f
    path = [root]
    while True:
        search_result = _ida_star_search(path, depth)
        if search_result[1][-1].is_goal:
            return search_result[1]
        depth = search_result[0]


def _ida_star_search(path, depth) -> (int, Node):
    """
    Recursive search function for solving the puzzle.
    :param path: list
        list of ancestor Nodes.
    :param depth: int
        maximum depth to expand to.
    :return: (int, Node)
        int - lowest f score found among the explored Nodes.
        Node - goal Node if found, the arg Node if not.
    """
    node = path[-1]
    if node.f > depth or node.is_goal:
        return node.f, path

    lowest_f = sys.maxsize
    for child in node.move():
        if child not in path:
            next_path = path + [child]
            search_result = _ida_star_search(next_path, depth)
            if search_result[1][-1].is_goal:
                return search_result[0], search_result[1]
            if lowest_f > search_result[0]:
                lowest_f = search_result[0]
    return lowest_f, path


def solve(puzzle) -> list:
    """
    Solves the 8-tile puzzle and prints results to stdout.
    :param puzzle: list
        8-tile puzzle state to be solved.
    :return: list
        list of 8-tile puzzle states that forms the path to the solution.
        Solution is at index [-1]. Initial state is at index [0].
    """
    global _move_counter
    _move_counter = 0  # reset global var

    start_time = time.time()
    solution = _ida_star(puzzle)[-1]
    end_time = time.time()

    print('-----------------------------------')
    print('initial state:', puzzle)
    print('number of moves:', solution.g)
    print('calls to move:', _move_counter)
    print('timer (seconds):', (end_time - start_time))
    print('-----------------------------------')
    return solution


def main():
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
        solve(Node(state))


if __name__ == '__main__':
    main()
