from a_Star import AStar
"""
    Make sure there is a path(goal is not blocked) and the starting point of player is not wall
"""
def check_asserts(ROWS, COLS, grid, start, goal, astar_start):
    sr, sc = start
    gr, gc = goal
    asr, asc = astar_start
    assert ROWS == len(grid), "Row size is incorrect"
    for row in grid:
        assert COLS == len(row), "Col size is incoreect"
    assert 0 <= sr < ROWS, "Player starting y invalid"
    assert 0 <= sc < COLS, "Player starting x invalid"
    assert grid[sr][sc] != 1, "Player starting point is wall"
    assert 0 <= gr < ROWS, "Goal y invalid"
    assert 0 <= gc < COLS, "Goal x invalid"
    assert grid[gr][gc] != 1, "Goal is wall"
    assert 0 <= asr < ROWS, "Astar Agent starting y invalid"
    assert 0 <= asc < COLS, "Astar Agent starting x invalid"
    assert grid[asr][asc] != 1, "Astar Agent starting point is wall"
    
    # "No path found"
    astar = AStar()
    path = astar.get_shortest_path(grid, start, goal)
    assert path is not None, "No path found"