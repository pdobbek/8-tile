import copy
import math
import sys
import time


goal_state = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]
goal_pos_dict = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }
move_counter = 0


class Node:
    """
    Class describing a state of an n-tile puzzle.
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
            co-ordinates of the 0 tile.
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
            True if this Node contains a state identical to the goal
            state. False otherwise.
        """
        return self.h == 0

    def __calculate_h(self) -> int:
        # expression to programmatically find goal row and column of any value,
        # for a puzzle of any size (doesn't have to be square). The goal state
        # has to follow format of 1, 2, 3, 4, 5, 6, .. 0.
        # v = value, n = number of column
        # (v-1)%n <- column
        # floor((v-1)/3) <- row
        h = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                goal_pos = self.__goal_position(self.grid[i][j])
                h += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
        return h

    def __goal_position(self, v) -> (int, int):
        n = len(self.grid[0])  # number of columns
        m = len(self.grid)  # number of rows
        if v == 0:
            return (n-1), (m-1)  # blank tile at the end of puzzle
        row = math.floor((v - 1) / n)
        column = (v - 1) % n
        return row, column

    def move(self):  # node
        """
        Generator which yields a new state for each possible move after moving
        the blank tile with _move_blank function.
        Doesn't change this state.
        Increment the move_counter global variable each time it's called.
        :return:
            new Node with state after blank tile move.
        """
        global move_counter
        move_counter += 1
        [i, j, grid] = self.state
        for pos in self._move_blank():
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
        solution 8-tile puzzle state that is the solution.
    """
    depth = root.f
    path = [root]
    while True:
        search_result = _ida_star_search(path, depth)
        if search_result[1].is_goal:
            return path
        depth = search_result[0]


def _ida_star_search(path, depth) -> (int, Node):
    node = path[-1]
    if node.f > depth:
        return node.f, node
    if node.is_goal:
        return node.f, node

    lowest_f = sys.maxsize
    for child in node.move():
        if child not in path:
            path.append(child)
            search_result = _ida_star_search(path, depth)
            if search_result[1].is_goal:
                return search_result[0], search_result[1]
            if search_result[0] < lowest_f:
                lowest_f = search_result[0]
            path.pop()
    return lowest_f, node


def solve(puzzle) -> list:
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
    solution = _ida_star(puzzle)[-1]
    end_time = time.time()

    print('-----------------------------------')
    print('initial state:', puzzle)
    print('number of moves:', solution.g)
    print('calls to move:', move_counter)
    print('timer (seconds):', (end_time - start_time))
    print('-----------------------------------')
    return solution


def main():
    global move_counter
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
