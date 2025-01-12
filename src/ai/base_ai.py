from abc import ABC, abstractmethod
from typing import List, Tuple

class BaseAI(ABC):
    @abstractmethod
    def choose_move(self, piles: List[int]) -> Tuple[int, int]:
        """Returns (pile_idx, candies) for the chosen move."""
        pass