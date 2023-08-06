#[cfg(test)]
mod astar_v2_tests {
    use crate::{astar_v2::{AStarV2, self}};

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
            vec![],
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (3, 5), (4, 5), (5, 5)]);
    }

    #[test]
    fn check_itr() {
        let mut a = astar_v2::AStarV2::new(
            vec![vec![]],
            (5, 5)
        );
        
        let occ_sqrs = vec![];
        
        let path = a.get_path_rust(
            (0, 0),
            (4, 4),
            occ_sqrs.clone(),
            vec![],
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]);

        let occ_sqrs2 = vec![vec![(2, 2), (2, 1), (2, 0)]];

        let path2 = a.get_path_rust(
            (0, 0),
            (4, 4),
            occ_sqrs2.clone(),
            occ_sqrs,
            true
        ).unwrap();

        assert_eq!(path2, vec![(0, 0), (1, 1), (1, 2), (2, 3), (3, 4), (4, 4)]);


        let occ_sqrs3 = vec![];

        let path2 = a.get_path_rust(
            (0, 0),
            (4, 4),
            occ_sqrs3,
            occ_sqrs2,
            true
        ).unwrap();

        assert_eq!(path2, vec![(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]);
    }
}