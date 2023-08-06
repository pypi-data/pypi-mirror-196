import aruw_pathfinding

astar = aruw_pathfinding.AStar()

start = (0, 0)
goal = (1, 1)
occupied_squares = []
grid_size = (2, 2)

path = astar.get_path(start, goal, occupied_squares, grid_size)

print(path)

dstar = aruw_pathfinding.DStar([], (3, 3))

start = (0, 0)
goal = (2, 2)
occupied_squares = []

path = dstar.get_path(start, goal, occupied_squares)

print(path)

path = dstar.get_path(start, goal, [[(1, 1)]])

print(path)

path = dstar.get_path(start, goal, [[(1, 1), (1, 0)]])

print(path)

try:
    path = dstar.get_path(start, goal, [[(1, 1), (1, 0), (0, 1)]])
    print(path)
except:
    print("Path not found")

path = dstar.get_path(start, goal, occupied_squares)