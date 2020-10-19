import copy  # used only in move(state) function.
import time  # used only in solve() function.

"""
-----------------------------------
initial state: [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]]
number of moves: 16
calls to move: 31240
timer (seconds): 0.8532953262329102
-----------------------------------
-----------------------------------
initial state: [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]]
number of moves: 18
calls to move: 88782
timer (seconds): 2.418712615966797
-----------------------------------
-----------------------------------
initial state: [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]]
number of moves: 20
calls to move: 187645
timer (seconds): 5.135307550430298
-----------------------------------
-----------------------------------
initial state: [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]]
number of moves: 18
calls to move: 108776
timer (seconds): 2.988727569580078
-----------------------------------
-----------------------------------
initial state: [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]]
number of moves: 18
calls to move: 69761
timer (seconds): 1.9120571613311768
-----------------------------------
-----------------------------------
initial state: [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]
number of moves: 18
calls to move: 86344
timer (seconds): 2.3629047870635986
-----------------------------------
-----------------------------------
initial state: [0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]]
number of moves: 20
calls to move: 252064
timer (seconds): 6.959729194641113
-----------------------------------
-----------------------------------
initial state: [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]]
number of moves: 14
calls to move: 6822
timer (seconds): 0.18247771263122559
-----------------------------------
-----------------------------------
initial state: [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]]
number of moves: 24
calls to move: 1737297
timer (seconds): 47.92298460006714
-----------------------------------
-----------------------------------
initial state: [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]]
number of moves: 22
calls to move: 571704
timer (seconds): 15.704419136047363
-----------------------------------
-----------------------------------
initial state: [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]
number of moves: 31
calls to move: 81492316
timer (seconds): 2452.2423148155212
-----------------------------------
"""
"""
Iterative Deepening Search program using Depth First Search to solve the
8-tile puzzle problem.

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
goal_state = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]
_move_counter = 0  # how many calls to the 'move' functions were performed


def is_goal(state):
    """
    Checks if the passed in puzzle state is the goal state.
    :param state: list
        puzzle state that is to be checked.
    :return: bool
        True if arg state is the solution. False if not.
    """
    for i in range(len(state[2])):  # for each row in state
        for j in range(len(state[2][i])):  # for each number in row
            if state[2][i][j] != goal_state[2][i][j]:
                return False  # if any numbers not the same as goal state
    return True


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


def move(state):
    """
    Generator which yields a new state for each possible move after moving
    the blank tile with move_blank function.
    Doesn't change the arg state.
    Increment the move_counter global variable each time it's called.
    :param state: list
        state to base the yielded states on.
    :return:
        state after blank tile move.
    """
    global _move_counter
    _move_counter += 1
    [i, j, grid] = state  # make note of current state
    n = len(grid)
    for pos in move_blank(i, j, n):
        i1, j1 = pos
        new_grid = copy.deepcopy(grid)
        new_grid[i][j], new_grid[i1][j1] = grid[i1][j1], grid[i][j]  # swap
        yield [i1, j1, new_grid]


def ids(root):
    """
    Begins the IDDFS search for solution to the puzzle passed. Solution
    is compared against the goal_state global variable.
    Currently loops indefinitely if the arg puzzle state cannot be
    solved.
    :param root: list
        8-tile puzzle state represented by a list of lists. I.e.
            [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]]
    :return: list
        list of Nodes that make up the path to the solution.
    """
    depth = 0
    path = [root]
    while True:
        depth += 1
        goal_path = dfs_cycle(path, depth)
        if goal_path is not None:
            return goal_path


def dfs_cycle(path, depth):
    """
    Iterative deepening depth first search algorithm with cycle
    detection using membership test.
    :param path: list
        set of puzzle states previously visited on the way to this
        state.
    :param depth: int
        maximum tree depth to expand the nodes to.
    :return:
        set of puzzle states the form a path to the solution. The
        last state is the solution.
        returns None if failed to find the solution.
    """
    if depth == 0 and is_goal(path[-1]):
        return path
    elif depth > 0:
        for next_state in move(path[-1]):
            if next_state not in path:
                next_path = path + [next_state]
                goal_path = dfs_cycle(next_path, depth - 1)
                if goal_path is not None:
                    return goal_path
    return None


def solve(puzzle):
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
    final_path = ids(puzzle)
    end_time = time.time()

    print('-----------------------------------')
    print('initial state: ' + puzzle.__str__())
    print('number of moves: ' + (len(final_path) - 1).__str__())
    print('calls to move: ' + _move_counter.__str__())
    print('timer (seconds): ' + (end_time - start_time).__str__())
    print('-----------------------------------')
    return final_path


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

    for puzzle in initial_states:
        solve(puzzle)


if __name__ == '__main__':
    main()
