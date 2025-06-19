from src.game.game import CandyGame
from src.ai.learning_ai import LearningAI
import os

def train_ai(episodes=10000, save_interval=1000):
    ai = LearningAI(load_path='models/ai_state.json')
    total_possible_states = 11 * 11 * 11  # 0-10 for each pile
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Fixed 3 piles
    for episode in range(episodes):
        # Create game with exactly 3 piles
        game = CandyGame(num_piles=3)
        game_history = []
        
        # Play the game
        while not game.is_game_over():
            current_state = tuple(game.piles)
            game_history.append(current_state)
            
            move = ai.choose_move(game.piles, training=True)
            if move:
                pile_idx, candies = move
                game.make_move(pile_idx, candies)
        
        # Learn from the game
        winner = 'AI' if len(game_history) % 2 == 0 else 'Opponent'
        ai.learn_from_game(game_history, winner)
        
        # Print progress
        if (episode + 1) % save_interval == 0:
            states_covered = len(ai.state_values)
            coverage_percent = (states_covered / total_possible_states) * 100
            
            print(f"\nEpisode {episode + 1}/{episodes}")
            print(f"States learned: {states_covered}/{total_possible_states} ({coverage_percent:.2f}%)")
            print(f"Example state values:")
            # Print some interesting states and their values
            test_states = [
                (1,0,0), # Simple winning position
                (2,2,2), # Equal piles
                (3,2,1), # Mixed position
            ]
            for state in test_states:
                value = ai.state_values.get(state, 0.0)
                print(f"State {state}: {value:.3f}")
            
            ai.save_state()
    
    return ai

if __name__ == "__main__":
    print("Starting AI training (3 piles only)...")
    trained_ai = train_ai()
    print("\nTraining complete!")
    
    # Print final statistics
    print("\nFinal State Values for key positions:")
    test_states = [
        (1,0,0), (2,0,0), (3,0,0),  # Single pile states
        (1,1,0), (2,2,0), (3,3,0),  # Two equal piles
        (1,1,1), (2,2,2), (3,3,3),  # Three equal piles
    ]
    for state in test_states:
        value = trained_ai.state_values.get(state, 0.0)
        print(f"State {state}: {value:.3f}")