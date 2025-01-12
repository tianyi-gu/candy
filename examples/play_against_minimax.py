from src.game.game import CandyGame
from src.ai.minimax_ai import MinimaxAI
from src.game.display import display_game_state

def main():
    game = CandyGame()
    ai = MinimaxAI()
    
    while not game.is_game_over():
        display_game_state(game.piles)
        
        # Player's turn
        while True:
            try:
                # Subtract 1 from user input to convert to 0-based index
                pile_idx = int(input(f"Choose pile (1-{len(game.piles)}): ")) - 1
                if pile_idx < 0 or pile_idx >= len(game.piles):
                    print("Invalid pile number!")
                    continue
                    
                candies = int(input(f"How many candies (1-{game.piles[pile_idx]}): "))
                if game.make_move(pile_idx, candies):
                    break
                print("Invalid move!")
            except ValueError:
                print("Please enter valid numbers!")
        
        if game.is_game_over():
            print("\nYou win!")
            break
            
        # AI's turn
        pile_idx, candies = ai.choose_move(game.piles)
        game.make_move(pile_idx, candies)
        print(f"\nAI takes {candies} candies from pile {pile_idx + 1}")  # Add 1 for display
        
        if game.is_game_over():
            display_game_state(game.piles)
            print("\nAI wins!")
            break

if __name__ == "__main__":
    main()