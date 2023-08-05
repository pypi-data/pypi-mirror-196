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
}