#[cfg(test)]
mod dstar_tests {
    use crate::{dstar};

    #[test]
    fn check_goal_is_start() {
        let mut a = dstar::DStar::new(
            vec![vec![]],
            (2, 2)
        );
        
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
        let mut a = dstar::DStar::new(
            vec![vec![]],
            (2, 2)
        );
        
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
        let mut a = dstar::DStar::new(
            vec![vec![]],
            (6, 6)
        );

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
        let mut a = dstar::DStar::new(
            vec![vec![]],
            (6, 6)
        );
        
        let occ_sqrs = vec![vec![(3, 1), (3, 2), (3, 3), (3, 4)]];
        
        let path = a.get_path_rust(
            (0, 0),
            (5, 5),
            occ_sqrs,
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (3, 5), (4, 5), (5, 5)]);
    }
    
    #[test]
    fn check_itr() {
        let mut a = dstar::DStar::new(
            vec![vec![]],
            (5, 5)
        );
        
        let occ_sqrs = vec![];
        
        let path = a.get_path_rust(
            (0, 0),
            (4, 4),
            occ_sqrs,
            true
        ).unwrap();

        assert_eq!(path, vec![(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]);

        let occ_sqrs2 = vec![vec![(2, 2), (2, 1), (2, 0)]];

        let path2 = a.get_path_rust(
            (0, 0),
            (4, 4),
            occ_sqrs2,
            true
        ).unwrap();

        assert_eq!(path2, vec![(0, 0), (1, 1), (1, 2), (2, 3), (3, 4), (4, 4)]);


        let occ_sqrs3 = vec![];

        let path2 = a.get_path_rust(
            (0, 0),
            (4, 4),
            occ_sqrs3,
            true
        ).unwrap();

        assert_eq!(path2, vec![(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]);
    }
}