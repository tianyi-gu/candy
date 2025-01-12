from src.game.game import CandyGame
from src.ai.learning_ai import LearningAI
import os
from datetime import datetime

def train_ai(episodes=500000, save_interval=10000):
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    
    # Try to load existing AI state
    ai = LearningAI(load_path='models/ai_state.json')
    
    wins = 0
    for episode in range(episodes):
        game = CandyGame()  # Will now always create 3 piles
        game_history = []
        
        while not game.is_game_over():
            current_state = tuple(game.piles)
            game_history.append(current_state)
            
            pile_idx, candies = ai.choose_move(game.piles, training=True)
            game.make_move(pile_idx, candies)
        
        # Learn from the game
        winner = 'AI' if len(game_history) % 2 == 0 else 'Opponent'
        if winner == 'AI':
            wins += 1
        ai.learn_from_game(game_history, winner)
        
        # Print progress and save periodically
        if (episode + 1) % save_interval == 0:
            win_rate = (wins / save_interval) * 100
            wins = 0  # Reset counter
            
            stats = ai.get_training_stats()
            print(f"\nEpisode {episode + 1}/{episodes}")
            print(f"Win rate over last {save_interval} games: {win_rate:.2f}%")
            print(f"States learned: {stats['total_states_learned']}")
            print(f"Average state value: {stats['avg_state_value']:.3f}")
            
            # Save the model
            ai.save_state()
            
    return ai

if __name__ == "__main__":
    print("Starting AI training...")
    trained_ai = train_ai()
    print("\nTraining complete!")
    
    # Save final state
    trained_ai.save_state()
    
    # Print final statistics
    final_stats = trained_ai.get_training_stats()
    print("\nFinal Training Statistics:")
    print(f"Total states learned: {final_stats['total_states_learned']}")
    print(f"Average state value: {final_stats['avg_state_value']:.3f}")
    print(f"Max state value: {final_stats['max_state_value']:.3f}")
    print(f"Min state value: {final_stats['min_state_value']:.3f}")