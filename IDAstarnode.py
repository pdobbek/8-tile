from IDAstarpuzzle import Puzzle
import copy
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
open_list = []
closed_list = []
move_counter = 0


class Node:

    def __init__(self, state):
        self.state = state
        self.h = None  # has to be manually initiated
        self.f = None
        self.g = None

    def initiate(self, g):
        self.h = self.calculate_h()  # has to be manually initiated
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
        # TODO: maybe could improve by checking how far off the tile is
        h = 0
        n = len(self.grid)
        for i in range(n):  # for each row in state
            for j in range(n):  # for each number in row
                if self.grid[2][i][j] != goal_state[2][i][j]:
                    h += 1  # if not the same as goal state
        return h

    def generate_children(self):
        for child in self.move():
            if child not in closed_list and child not in open_list:
                if
                open_list.append(child)

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
            yield Node([i1, j1, new_grid])

    def __contains__(self, item):
        return self.grid == item.grid

    def __eq__(self, other):
        return self.grid == other.grid

    def __str__(self):
        return self.state.__str__()


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


def main():
    grid = Node([2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]])
    item = Node([2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]])
    print("__contains ok" if grid == item else "__contains__ ERROR")
    print("__eq__ ok" if grid in [item] else "__eq__ ERROR")

    for grid_child in grid.move():
        print(grid_child.__str__())


if __name__ == '__main__':
    main()
