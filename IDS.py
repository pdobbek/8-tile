import copy


def move_blank(i, j, n):
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
    [i, j, grid] = state  # make note of current state
    n = len(grid)
    for pos in move_blank(i, j, n):
        i1, j1 = pos
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]  # swap
        yield [i1, j1, grid]
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]  # swap back


def get_all_moves(node, memory):
    all_moves = set()
    for next_state in move(node):
        temp = copy.deepcopy(next_state)
        if temp not in memory:
            all_moves.add(temp)
    return all_moves


def search(root, goal_state):
    depth = 0
    memory = set()
    while True:
        depth += 1
        found, remaining = depth_limited(root, depth, goal_state, memory)
        if found is not None:
            return found
        elif not remaining:
            return None


def depth_limited(node, depth, goal_state, memory):
    print('Current node: ' + node.__str__())

    if depth == 0:
        if node is goal_state:
            return node, True
        else:
            return None, True  # not a solution, but might have children
    elif depth > 0:
        any_remaining = False
        for child in get_all_moves(node, memory):
            found, remaining = depth_limited(child, depth-1, goal_state,
                                             memory)
            if found is not None:
                return found, True
            if remaining is True:
                any_remaining = True  # at least one node found. Deepen search.
        return None, any_remaining


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
    goal_state = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]

    first_goal = search(initial_states[0], goal_state)
    print(first_goal.__str__())


if __name__ == '__main__':
    main()
