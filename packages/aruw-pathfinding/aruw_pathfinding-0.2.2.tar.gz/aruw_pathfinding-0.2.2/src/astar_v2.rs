use priority_queue::PriorityQueue;
use pyo3::prelude::*;
use pyo3::exceptions::PyTypeError;
use pyo3::types::{PyList, PyTuple};

struct Node {
    permanent_occupied: bool,
    dynamic_occupied: bool,
    f: i32,
    g: i32,
    h: i32,
    parent: Option<(usize, usize)>,
}

#[pyclass]
pub struct AStarV2 {
    // first_time: bool,
    grid: Vec<Vec<Node>>,
    grid_size: (usize, usize),
}

impl AStarV2 {
    fn get_g(parent: (usize, usize), pt: (usize, usize)) -> i32 {
        if parent.0 == pt.0 || parent.1 == pt.1 {
            10
        } else {
            14
        }
    }

    fn get_h(destination: (usize, usize), pt: (usize, usize)) -> i32 {
        let dx = (destination.0 as i32 - pt.0 as i32).abs();
        let dy = (destination.1 as i32 - pt.1 as i32).abs();
        if dx > dy {
            14 * dy + 10 * (dx - dy)
        } else {
            14 * dx + 10 * (dy - dx)
        }
    }

    fn get_parent(&self, pt: (usize, usize)) -> (usize, usize) {
        self.grid[pt.0][pt.1].parent.unwrap()
    }

    pub fn get_path_rust(
        &mut self,
        start: (usize, usize),
        goal: (usize, usize),
        occupied_squares: Vec<Vec<(usize, usize)>>,
        debug: bool,
    ) -> Result<Vec<(usize, usize)>, &'static str> {

        (0..self.grid_size.0).for_each(|i| (0..self.grid_size.1).for_each(
            |j| self.grid[i][j].dynamic_occupied = false
        ));

        // occupied_squares.iter().for_each(|arr| arr.iter().for_each(
        //     |&pt| self.grid[pt.0][pt.1].dynamic_occupied = true
        // ));

        occupied_squares.iter().flatten().for_each(
            |&pt| self.grid[pt.0][pt.1].dynamic_occupied = true
        );

        let mut open_list = PriorityQueue::new();
        let mut closed_list: Vec<(usize, usize)> = Vec::new();

        open_list.push(goal, 0);
        self.grid[goal.0][goal.1].f = 0;

        let mut target_found = false;

        while open_list.len() > 0 && !target_found {
            let (pt, _) = open_list.pop().unwrap();

            if debug {
                println!("looking at point: {:?}", pt);
            }

            if pt == start {
                if debug {
                    println!("found start!");
                }
                target_found = true;
                break; // we're done!
            }

            for xmod in 0..3 {
                for ymod in 0..3 {
                    if xmod == 1 && ymod == 1 {
                        continue;
                    }

                    if (pt.0 + xmod) as i32 - 1 < 0 || pt.0 + xmod - 1 >= self.grid_size.0
                    || (pt.1 + ymod) as i32 - 1 < 0 || pt.1 + ymod - 1 >= self.grid_size.1 {
                        // println!("out of bounds");
                        continue;
                    }
                    
                    let new_pt = ((pt.0 + xmod - 1), (pt.1 + ymod - 1));

                    if self.grid[new_pt.0][new_pt.1].dynamic_occupied {
                        continue;
                    }
                    
                    if self.grid[new_pt.0][new_pt.1].permanent_occupied {
                        continue;
                    }
                    
                    let check_open_list = open_list.get_priority(&new_pt);
                    
                    let g = Self::get_g(pt, new_pt) + self.grid[pt.0][pt.1].g;
                    let h = Self::get_h(start, new_pt);
                    let f = g + h;
                    
                    if closed_list.contains(&new_pt) {
                        // continue;
                        if self.grid[new_pt.0][new_pt.1].f < f {
                            continue;
                        }
                    }

                    if check_open_list != None {
                        if (*check_open_list.unwrap() as i32).abs() < f {
                            continue;
                        }
                    }

                    let mut node = &mut self.grid[new_pt.0 as usize][new_pt.1 as usize];

                    node.g = g;
                    node.h = h;
                    node.f = f;
                    node.parent = Some(pt);

                    open_list.push(new_pt, -f);

                    if debug {
                        println!("new_pt: {:?}, g: {}, h: {}, f: {}", new_pt, g, h, f);
                    }
                }
            }

            closed_list.push(pt);
        }        

        if !target_found {
            return Err("Target not found");
        }

        let mut path: Vec<(usize, usize)> = Vec::new();
        let mut curr = start;

        while curr != goal {
            path.push(curr);
            curr = Self::get_parent(&self, curr);
        }
        
        path.push(goal);

        if debug {
            println!("path: {:?}", path);
        }

        Ok(path)
    }
}

#[pymethods]
impl AStarV2 {
    #[new]
    pub fn new(
        occupied_squares: Vec<Vec<(usize, usize)>>,
        grid_size: (usize, usize)
    ) -> Self {
        let mut grid: Vec<Vec<Node>> = Vec::new();
        for _x in 0..grid_size.0 {
            let mut row: Vec<Node> = Vec::new();
            for _y in 0..grid_size.1 {
                row.push(Node {
                    permanent_occupied: false,
                    dynamic_occupied: false,
                    f: 0,
                    g: 0,
                    h: 0,
                    parent: None,
                });
            }
            grid.push(row);
        }

        occupied_squares.iter().flatten().for_each(
            |&pt| grid[pt.0][pt.1].permanent_occupied = true
        );

        AStarV2 {
            grid: grid,
            grid_size: grid_size,
        }
    }

    pub fn get_path(
        &mut self,
        _py: Python,
        start: (usize, usize),
        goal: (usize, usize),
        occupied_squares: Vec<Vec<(usize, usize)>>,
    ) -> PyResult<Py<PyList>> {
        let path_res = Self::get_path_rust(self, start, goal, occupied_squares, false);
        return match path_res {
            Ok(path) => {
                let python_path = PyList::empty(_py);
                for node in path.into_iter() {
                    let py_tuple = PyTuple::new(_py, &[node.0.into_py(_py), node.1.into_py(_py)]);
                    python_path.append(py_tuple)?;
                }
        
                Ok(python_path.into_py(_py))
            },
            Err(error) => Err(PyErr::new::<PyTypeError, _>(error)),
        }
    }
}
