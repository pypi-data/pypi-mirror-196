use pyo3::prelude::*;
mod astar;
mod dstar;
mod dstar_tests;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn aruw_pathfinding(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<astar::AStar>()?;
    m.add_class::<dstar::DStar>()?;
    Ok(())
}

#[cfg(test)]
mod astar_tests {
    use crate::{astar};

    #[test]
    fn check_goal_is_start() {
        let mut a = astar::AStar::new();
        
        let path = a.get_path_rust(
            (0, 0),
            (0, 0),
            vec![],
            (2, 2),
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0)]);
    }
    
    #[test]
    fn check_goal_one_away_start() {
        let mut a = astar::AStar::new();
        
        let path = a.get_path_rust(
            (0, 0),
            (1, 1),
            vec![],
            (2, 2),
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1)]);
    }
    
    #[test]
    fn check_larger_empty() {
        let mut a = astar::AStar::new();
        
        let path = a.get_path_rust(
            (0, 0),
            (5, 5),
            vec![],
            (6, 6),
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]);
    }
    
    #[test]
    fn check_larger_with_wall() {
        let mut a = astar::AStar::new();
        let occ_sqrs = vec![vec![(3, 1), (3, 2), (3, 3), (3, 4)]];
        
        let path = a.get_path_rust(
            (0, 0),
            (5, 5),
            occ_sqrs,
            (6, 6),
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (3, 5), (4, 5), (5, 5)]);
    }
}
