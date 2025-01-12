from typing import List, Tuple
import random

class CandyGame:
    def __init__(self):
        """Initialize game with exactly 3 piles"""
        self.piles = [random.randint(1, 10) for _ in range(3)]
        
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