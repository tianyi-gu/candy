from typing import List, Tuple
import random

class CandyGame:
    def __init__(self, num_piles=3, min_candies=2, max_candies=10):
        """
        Initialize game with customizable number of piles
        
        Args:
            num_piles (int): Number of piles (default: 3)
            min_candies (int): Minimum candies per pile (default: 2)
            max_candies (int): Maximum candies per pile (default: 10)
        """
        if not (2 <= num_piles <= 10):
            raise ValueError("Number of piles must be between 2 and 10")
        if min_candies < 2:
            raise ValueError("Minimum candies must be at least 2")
        if max_candies < min_candies:
            raise ValueError("Maximum candies must be greater than minimum")
            
        self.piles = [random.randint(min_candies, max_candies) 
                     for _ in range(num_piles)]
        
    def make_move(self, pile_idx: int, candies: int) -> bool:
        """Attempt to make a move. Returns True if valid, False otherwise."""
        if not (0 <= pile_idx < len(self.piles)):
            return False
        if not (1 <= candies <= self.piles[pile_idx]):
            return False
            
        self.piles[pile_idx] -= candies
        return True
    
    def is_game_over(self) -> bool:
        return sum(self.piles) == 0
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Returns list of valid moves as (pile_idx, candies) tuples."""
        moves = []
        for pile_idx in range(len(self.piles)):
            for candies in range(1, self.piles[pile_idx] + 1):
                moves.append((pile_idx, candies))
        return moves