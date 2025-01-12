import random
import numpy as np
import json
import os

class LearningAI:
    def __init__(self, load_path=None):
        self.state_values = {}
        self.learning_rate = 0.1
        self.epsilon = 0.1
        
        # Load previous training if available
        if load_path and os.path.exists(load_path):
            self.load_state(load_path)
    
    def save_state(self, save_path='models/ai_state.json'):
        """Save the learned state values to a file"""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Convert state_values keys to strings (as JSON requires string keys)
        state_dict = {str(k): v for k, v in self.state_values.items()}
        
        with open(save_path, 'w') as f:
            json.dump(state_dict, f)
            
    def load_state(self, load_path='models/ai_state.json'):
        """Load the learned state values from a file"""
        with open(load_path, 'r') as f:
            state_dict = json.load(f)
            # Convert string keys back to tuples
            self.state_values = {tuple(map(int, k.strip('()').split(','))): v 
                               for k, v in state_dict.items()}
    
    def get_training_stats(self):
        """Return statistics about the training"""
        return {
            'total_states_learned': len(self.state_values),
            'avg_state_value': np.mean(list(self.state_values.values())),
            'max_state_value': max(self.state_values.values()),
            'min_state_value': min(self.state_values.values())
        }
    
    def get_state_key(self, piles):
        # Convert piles to a hashable tuple, sorted to handle equivalent states
        return tuple(sorted(piles))
        
    def choose_move(self, piles, training=False):
        possible_moves = []
        for pile_idx, count in enumerate(piles):
            for candies in range(1, count + 1):
                new_piles = list(piles)
                new_piles[pile_idx] -= candies
                state_key = self.get_state_key(new_piles)
                value = self.state_values.get(state_key, 0.0)
                
                # During training, add some randomness to value
                if training:
                    # Add noise to encourage exploration of different moves
                    value += random.uniform(-0.1, 0.1)
                    
                possible_moves.append((pile_idx, candies, value))
        
        if not possible_moves:
            return None
        
        # During training, sometimes take random amounts
        if training and random.random() < self.epsilon:
            pile_idx, count = random.choice([(i, c) for i, c, _ in possible_moves])
            # Encourage taking different amounts, not just 1
            candies = random.randint(1, count)
            return pile_idx, candies
        
        # Choose move with highest expected value
        best_value = max(move[2] for move in possible_moves)
        best_moves = [(i, c) for i, c, v in possible_moves if v >= best_value - 0.000001]
        
        return random.choice(best_moves)
        
    def learn_from_game(self, game_history, winner):
        reward = 1 if winner == 'AI' else -1
        
        # Update state values backwards with future consideration
        for i in range(len(game_history)-1, -1, -1):
            state = game_history[i]
            state_key = tuple(sorted(state))
            
            # Is it AI's turn? (even indices are AI turns in history)
            is_ai_turn = (len(game_history) - 1 - i) % 2 == 0
            
            # If it's player's turn, this state should have opposite value
            if not is_ai_turn:
                reward = -reward
            
            current_value = self.state_values.get(state_key, 0.0)
            # Bigger adjustment for states closer to end
            adjustment = self.learning_rate * (1 + (len(game_history) - i) / len(game_history))
            self.state_values[state_key] = current_value + adjustment * (reward - current_value)

    def is_winning_state(self, piles):
        """Check if this is a winning state using minimax for small states"""
        total_candies = sum(piles)
        if total_candies <= 3:  # Small enough to calculate exactly
            return self.calculate_minimax(piles) > 0
        return False

    def verify_state_value(self, state, value):
        """Verify that a state's value makes sense"""
        total_candies = sum(state)
        if total_candies == 1:
            # States with only one candy should be losing positions for AI
            return -1.0
        if total_candies == 2 and max(state) == 2:
            # States with (2,0,0) are winning positions
            return 1.0
        return value