#[cfg(test)]
mod astar_v2_tests {
    use crate::{astar_v2::AStarV2};

    fn get_new(
        occupied_squares: Vec<Vec<(usize, usize)>>,
        grid_size: (usize, usize),
    ) -> AStarV2 {
        AStarV2::new(
            occupied_squares,
            grid_size,
        )
    }

    fn get_2x2_unoccupied() -> AStarV2 {
        get_new(vec![], (2, 2))
    }

    fn get_6x6_unoccupied() -> AStarV2 {
        get_new(vec![], (6, 6))
    }

    #[test]
    fn check_goal_is_start() {
        let mut a = get_2x2_unoccupied();
        
        let path = a.get_path_rust(
            (0, 0),
            (0, 0),
            vec![],
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0)]);
    }
    
    #[test]
    fn check_goal_one_away_start() {
        let mut a = get_2x2_unoccupied();
        
        let path = a.get_path_rust(
            (0, 0),
            (1, 1),
            vec![],
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1)]);
    }
    
    #[test]
    fn check_larger_empty() {
        let mut a = get_6x6_unoccupied();
        
        let path = a.get_path_rust(
            (0, 0),
            (5, 5),
            vec![],
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]);
    }
    
    #[test]
    fn check_larger_with_wall() {
        let mut a = get_6x6_unoccupied();
        let occ_sqrs = vec![vec![(3, 1), (3, 2), (3, 3), (3, 4)]];
        
        let path = a.get_path_rust(
            (0, 0),
            (5, 5),
            occ_sqrs,
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (3, 5), (4, 5), (5, 5)]);
    }
}