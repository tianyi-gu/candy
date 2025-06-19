import random
import numpy as np
import json
import os

class LearningAI:
    def __init__(self, load_path=None):
        self.state_values = {}
        self.learning_rate = 0.3
        self.epsilon = 0.3
        self.discount_factor = 0.95
        
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
        if not training:
            print(f"\nAI analyzing position: {piles}")
        
        # CASE 1: If there's only one pile with candies, take all of them
        non_empty_piles = [(i, count) for i, count in enumerate(piles) if count > 0]
        if len(non_empty_piles) == 1:
            pile_idx, count = non_empty_piles[0]
            if not training:
                print(f"Only one pile left, taking all {count} candies from pile {pile_idx + 1}")
            return pile_idx, count
        
        # CASE 2: If there are two non-empty piles, take all from larger pile
        if len(non_empty_piles) == 2:
            pile1_idx, count1 = non_empty_piles[0]
            pile2_idx, count2 = non_empty_piles[1]
            if count1 >= count2:
                if not training:
                    print(f"Two piles left, taking all {count1} candies from pile {pile1_idx + 1}")
                return pile1_idx, count1
            else:
                if not training:
                    print(f"Two piles left, taking all {count2} candies from pile {pile2_idx + 1}")
                return pile2_idx, count2
        
        # CASE 3: For other positions, try to make a smart move
        possible_moves = []
        for pile_idx, count in enumerate(piles):
            for candies in range(1, count + 1):
                new_piles = list(piles)
                new_piles[pile_idx] -= candies
                
                # Prefer taking more candies
                move_value = candies / sum(piles)
                possible_moves.append((pile_idx, candies, move_value))
                
                if not training:
                    print(f"Evaluating: Take {candies} from pile {pile_idx + 1} -> Value: {move_value:.3f}")
        
        if not possible_moves:
            return None
        
        # Choose move with highest value
        best_value = max(move[2] for move in possible_moves)
        best_moves = [(i, c, v) for i, c, v in possible_moves if v >= best_value - 0.000001]
        
        # Among best moves, prefer taking more candies
        max_candies = max(c for _, c, _ in best_moves)
        best_moves = [(i, c, v) for i, c, v in best_moves if c == max_candies]
        
        chosen = random.choice(best_moves)
        if not training:
            print(f"Choosing: Take {chosen[1]} from pile {chosen[0] + 1}")
        
        return chosen[0], chosen[1]
    
    def learn_from_game(self, game_history, winner):
        """Update state values based on game outcome"""
        reward = 1.0 if winner == 'AI' else -1.0
        
        # Process game history backwards
        for idx, state in enumerate(reversed(game_history)):
            state_key = tuple(sorted(state))
            current_value = self.state_values.get(state_key, 0.0)
            
            # Larger updates for states closer to end
            position_weight = (idx + 1) / len(game_history)
            update = self.learning_rate * position_weight * (reward - current_value)
            
            # Winning moves should always have high value
            if idx == 0 and winner == 'AI':
                self.state_values[state_key] = max(0.9, current_value + update)
            else:
                self.state_values[state_key] = current_value + update
            
            # Flip reward for opponent's turn
            reward = -reward * self.discount_factor

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