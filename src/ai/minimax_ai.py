from typing import List, Tuple, Dict
from .base_ai import BaseAI
from ..utils.state_utils import get_state_key

class MinimaxAI(BaseAI):
    def __init__(self):
        self.memo: Dict = {}
    
    def choose_move(self, piles: List[int]) -> Tuple[int, int]:
        winning_moves = self._get_winning_moves(piles)
        if winning_moves:
            return winning_moves[0]
        return self._get_any_valid_move(piles)
    
    def _get_winning_moves(self, piles: List[int]) -> List[Tuple[int, int]]:
        # Implementation from previous minimax code
        pass
    
    def _get_any_valid_move(self, piles):
        """
        Returns any valid move from the current position.
        Used as a fallback when no winning move is found.
        
        Args:
            piles: List of integers representing the candy piles
            
        Returns:
            tuple: (pile_index, number_of_candies)
        """
        # Find first non-empty pile and take one candy
        for i, pile in enumerate(piles):
            if pile > 0:
                return (i, 1)
        return (0, 0)  # Should never reach here if game is not over