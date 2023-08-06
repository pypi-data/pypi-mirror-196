# Pathfinding project for ARUW sentry

> Built in rust for speed and safety

## AStar Usage

```py
import aruw_pathfinding

astar = aruw_pathfinding.AStar()

start = (0, 0)
goal = (2, 2)
occupied_squares = []
grid_size = (3, 3)

path: List[Tuple[int, int]]

try:
    path = astar.get_path(start, goal, occupied_squares, grid_size)
except:
    print("Path not found")
```

## DStar Usage

```py
from typing import List, Tuple
import aruw_pathfinding

initial_occupied_squares: List[List[Tuple[int, int]]] = []
grid_size = (3, 3)

# Initialize the algorithm
dstar = aruw_pathfinding.DStar(
    initial_occupied_squares,
    grid_size,
)

# For each get_path iteration
start = (0, 0)
goal = (2, 2)
occupied_squares: List[List[Tuple[int, int]]] = []

path: List[Tuple[int, int]]

# initial iteration
try:
    path = dstar.get_path(start, goal, occupied_squares)
except:
    print("Path not found")

print(path) # will be [(0, 0), (1, 1), (2, 2)]

occupied_squares = [[(1, 1)]]
# same calling syntax for more iterations
try:
    path = dstar.get_path(start, goal, occupied_squares)
except:
    print("Path not found")

print(path) # will be [(0, 0), (1, 0), (2, 1), (2, 2)]
```