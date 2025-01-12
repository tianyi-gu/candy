from typing import List, Tuple, Dict
import random
from .base_ai import BaseAI
from ..utils.state_utils import get_state_key

class QLearningAI(BaseAI):
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.q_table: Dict = {}
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
    
    def choose_move(self, piles: List[int]) -> Tuple[int, int]:
        if random.random() < self.epsilon:
            return self._get_random_move(piles)
        return self._get_best_move(piles)