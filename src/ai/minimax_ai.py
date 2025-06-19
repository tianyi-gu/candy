from typing import List, Tuple, Dict
from .base_ai import BaseAI
from ..utils.state_utils import get_state_key

class MinimaxAI(BaseAI):
    def __init__(self):
        self.memo: Dict[str, bool] = {}
    
    def choose_move(self, piles: List[int]) -> Tuple[int, int]:
        winning_moves = self._get_winning_moves(piles)
        if winning_moves:
            return winning_moves[0]
        return self._get_any_valid_move(piles)
    
    def _is_winning_state(self, piles: List[int]) -> bool:
        state_key = get_state_key(piles)
        if state_key in self.memo:
            return self.memo[state_key]

        for i, pile_size in enumerate(piles):
            for k in range(1, pile_size + 1):
                next_piles = piles[:]
                next_piles[i] -= k
                if not self._is_winning_state(next_piles):
                    self.memo[state_key] = True
                    return True

        self.memo[state_key] = False
        return False
    
    def _get_winning_moves(self, piles: List[int]) -> List[Tuple[int, int]]:
        winning_moves = []
        for i, pile_size in enumerate(piles):
            for k in range(1, pile_size + 1):
                next_piles = piles[:]
                next_piles[i] -= k
                if not self._is_winning_state(next_piles):
                    winning_moves.append((i, k))
        return winning_moves
    
    def _get_any_valid_move(self, piles):
        """
        Returns any valid move from the current position.
        Used as a fallback when no winning move is found.
        
        Args:
            piles: List of integers representing the candy piles
            
        Returns:
            tuple: (pile_index, number_of_candies)
        """
        for i, pile in enumerate(piles):
            if pile > 0:
                return (i, 1)
        return (0, 0)  # Should never reach here if game is not over