# Pathfinding project for ARUW sentry

Written with [pyo3](https://pyo3.rs/main/doc/pyo3/#) using maturin

More pyo3 [docs](https://pyo3.rs/v0.17.3/python_typing_hints.html)

[pyi typing hints](https://pyo3.rs/v0.17.3/python_typing_hints.html#my_projectpyi-content)

## Compiling

```
maturin develop
```

## Testing

The rust tests work as desired despite documents stating that it wouldn't work.

```
cargo test
```

In Python:

```py
import aruw_pathfinding

astar = aruw_pathfinding.AStar()

start = (0, 0)
goal = (1, 1)
occupied_squares = []
grid_size = (2, 2)

path = astar.get_path(start, goal, occupied_squares, grid_size)
```

## Look here in the future

- https://github.com/PyO3/pyo3
- https://github.com/mdeyo/d-star-lite/blob/master/grid.py

