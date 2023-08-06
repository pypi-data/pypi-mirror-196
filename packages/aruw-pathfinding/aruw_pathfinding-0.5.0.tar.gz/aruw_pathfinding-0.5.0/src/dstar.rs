use priority_queue::PriorityQueue;
use pyo3::prelude::*;
use pyo3::exceptions::PyTypeError;
use pyo3::types::{PyList, PyTuple};

struct Node {
    occupied: bool,
    // x: usize,
    // y: usize,
    f: i32,
    g: i32,
    h: i32,
    parent: Option<(usize, usize)>,
    children: Vec<(usize, usize)>,
    // parent: Option<Box<Node>>,
}

#[pyclass]
pub struct DStar {
    // first_time: bool,
    grid: Vec<Vec<Node>>,
    grid_size: (usize, usize),
    // old_grid: Vec<Vec<Node>>,
    old_start: (usize, usize),
    old_goal: (usize, usize),
    // old_open_list: &'static PriorityQueue<(usize, usize), i32>,
    // old_closed_list: &'static Vec<(usize, usize)>,
    // old_open_list: PriorityQueue<(usize, usize), i32>,
    // old_closed_list: Vec<(usize, usize)>,
    open_list: PriorityQueue<(usize, usize), i32>,
    closed_list: Vec<(usize, usize)>,
    old_inst_occ_squares: Vec<Vec<(usize, usize)>>,
}

impl DStar {
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

    fn remove_from_closed_list(&mut self, pt: (usize, usize)) {
        let closed_idx_res = self.closed_list.iter().position(|&check_pt| check_pt == pt);

        if closed_idx_res != None {
            self.closed_list.remove(closed_idx_res.unwrap());
        }
    }

    fn closed_neighbors_to_open_list(&mut self, vec: &Vec<Vec<(usize, usize)>>) {
        for arr in vec.iter() {
            for pt in arr.iter() {
                for xmod in 0..3 {
                    for ymod in 0..3 {
                        if xmod == 1 && ymod == 1 {
                            continue;
                        }

                        if (pt.0 + xmod) as i32 - 1 < 0
                            || pt.0 + xmod - 1 >= self.grid_size.0
                            || (pt.1 + ymod) as i32 - 1 < 0
                            || pt.1 + ymod - 1 >= self.grid_size.1
                        {
                            // println!("out of bounds");
                            continue;
                        }

                        let new_pt = ((pt.0 + xmod - 1), (pt.1 + ymod - 1));

                        if self.grid[new_pt.0][new_pt.1].occupied {
                            continue;
                        }

                        let closed_idx_res =
                            self.closed_list.iter().position(|&check_pt| check_pt == new_pt);

                        if closed_idx_res != None {
                            self.closed_list.remove(closed_idx_res.unwrap());
                            // self.open_list.push(new_pt, self.grid[pt.0][pt.1].f);
                            self.open_list.push(new_pt, 1);
                        }
                    }
                }
            }
        }
    }

    pub fn get_path_rust(
        &mut self,
        start: (usize, usize),
        goal: (usize, usize),
        occupied_squares: Vec<Vec<(usize, usize)>>,
        debug: bool,
    ) -> Result<Vec<(usize, usize)>, &'static str> {
        let mut old_squares: Vec<Vec<(usize, usize)>> = Vec::new();
        for arr in self.old_inst_occ_squares.iter() {
            let mut vec: Vec<(usize, usize)> = Vec::new();
            for &pt in arr.iter() {
                self.grid[pt.0][pt.1].occupied = false;
                vec.push(pt);
            }
            old_squares.push(vec);
        }

        for arr in occupied_squares.iter() {
            for &pt in arr.iter() {
                // println!("Removing pt: {:?}", pt);
                self.grid[pt.0][pt.1].occupied = true;

                let mut unvisited_children: Vec<(usize, usize)> = vec![];
                // let mut visited_children: Vec<(usize, usize)> = vec![];

                unvisited_children.push(pt);
                while unvisited_children.len() > 0 {
                    let child = unvisited_children.pop().unwrap();
                    self.remove_from_closed_list(child);
                    self.open_list.remove(&child);
                    // visited_children.push(child);
                    self.grid[child.0][child.1].parent = None;

                    self.grid[child.0][child.1]
                        .children
                        .iter()
                        .for_each(|&ch| unvisited_children.push(ch));

                    self.grid[child.0][child.1].children = vec![];
                }
            }
        }

        if start == self.old_start && goal == self.old_goal {
            // add squares in closed list touching all touched
            //          occupied_squares into the open_list
            self.closed_neighbors_to_open_list(&old_squares);
            self.closed_neighbors_to_open_list(&occupied_squares);
        } else {
            self.open_list = PriorityQueue::new();
            self.closed_list = Vec::new();

            self.open_list.push(goal, 0);
            self.grid[goal.0][goal.1].f = 0;
        }

        let mut target_found = false;

        // println!("cl: {:?}", self.closed_list);
        // let open_list = &self.open_list;
        // print!("ol: ");
        // for item in open_list.into_iter() {
        //     print!("{:?}, ", item.0);
        // }
        // println!("");

        while self.open_list.len() > 0 && !target_found {
            let (pt, _) = self.open_list.pop().unwrap();
            self.closed_list.push(pt);

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

                    if (pt.0 + xmod) as i32 - 1 < 0
                        || pt.0 + xmod - 1 >= self.grid_size.0
                        || (pt.1 + ymod) as i32 - 1 < 0
                        || pt.1 + ymod - 1 >= self.grid_size.1
                    {
                        // println!("out of bounds");
                        continue;
                    }

                    let new_pt = ((pt.0 + xmod - 1), (pt.1 + ymod - 1));

                    if self.grid[new_pt.0][new_pt.1].occupied {
                        continue;
                    }

                    let check_open_list = self.open_list.get_priority(&new_pt);

                    let g = Self::get_g(pt, new_pt) + self.grid[pt.0][pt.1].g;
                    let h = Self::get_h(start, new_pt);
                    let f = g + h;

                    if self.closed_list.contains(&new_pt) {
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

                    let node_read_only = &self.grid[new_pt.0 as usize][new_pt.1 as usize];
                    if node_read_only.parent != None {
                        let parent = node_read_only.parent.unwrap();
                        let idx = self.grid[parent.0][parent.1]
                            .children
                            .iter()
                            .position(|&pt| pt == new_pt)
                            .unwrap();
                        self.grid[parent.0][parent.1].children.remove(idx);
                    }

                    let mut node = &mut self.grid[new_pt.0 as usize][new_pt.1 as usize];

                    node.g = g;
                    node.h = h;
                    node.f = f;
                    node.parent = Some(pt);
                    self.grid[pt.0][pt.1].children.push(new_pt);

                    self.open_list.push(new_pt, -f);

                    if debug {
                        println!("new_pt: {:?}, g: {}, h: {}, f: {}", new_pt, g, h, f);
                    }
                }
            }
        }

        self.old_inst_occ_squares = occupied_squares;
        self.old_goal = goal;
        self.old_start = start;

        // println!("cl: {:?}", self.closed_list);
        // let open_list = &self.open_list;
        // print!("ol: ");
        // for item in open_list.into_iter() {
        //     print!("{:?}, ", item.0);
        // }
        // println!("");

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
impl DStar {
    #[new]
    pub fn new(occupied_squares: Vec<Vec<(usize, usize)>>, grid_size: (usize, usize)) -> Self {
        let mut grid: Vec<Vec<Node>> = Vec::new();
        for _x in 0..grid_size.0 {
            let mut row: Vec<Node> = Vec::new();
            for _y in 0..grid_size.1 {
                row.push(Node {
                    occupied: false,
                    f: 0,
                    g: 0,
                    h: 0,
                    parent: None,
                    children: vec![],
                });
            }
            grid.push(row);
        }

        for arr in occupied_squares.iter() {
            for pt in arr.iter() {
                grid[pt.0][pt.1].occupied = true;
            }
        }

        let mut open_list: PriorityQueue<(usize, usize), i32> = PriorityQueue::new();

        open_list.push((0, 0), 0);
        grid[0][0].f = 0;

        DStar {
            grid: grid,
            // old_grid: grid,
            grid_size: grid_size,
            old_start: (0, 0),
            old_goal: (0, 0),
            open_list: open_list,
            closed_list: vec![],
            old_inst_occ_squares: vec![],
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
