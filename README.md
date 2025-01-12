# Candy Game with AI

A simple turn-based candy game where players compete against an AI to take candies from multiple piles. The AI learns strategies through self-play reinforcement learning.

## Game Rules

- The game starts with n piles of candies (n is between 2 and 10)
- Each pile contains a random number of candies (between 1 and 10)
- Players take turns removing candies from piles
- On each turn, a player can take any number of candies from a single pile
- The player who takes the last candy wins

## AI Implementation

The game features a Learning AI that:
- Uses reinforcement learning through self-play
- Learns strategies by playing against itself
- Features:
  - State-value mapping for decision making
  - Epsilon-greedy exploration during training
  - Random noise addition for move diversity
  - Experience-based learning
  - Can handle larger state spaces efficiently

## Project Structure

- `src/game/game.py`: Defines the game logic and state representation
- `src/ai/base_ai.py`: Base class for AI implementations
- `src/ai/minimax_ai.py`: Minimax AI implementation
- `src/ai/learning_ai.py`: Reinforcement learning AI implementation
- `tests/test_game.py`: Unit tests for the game logic
- `examples/play_against_minimax.py`: Example script to play against the Minimax AI
- `examples/train_ai.py`: Example script to train the Learning AI through self-play

## virtual environment
```bash
python -m venv candy 
source candy/bin/activate
pip install -r requirements.txt
```

## Running the Game

1. Train and play against the Learning AI:
```bash
python examples/play_against_ai.py
```
python examples/train_ai.py

2. Play against the Minimax AI:
```bash
python examples/play_against_minimax.py
```

## Testing
```bash
python -m unittest tests/test_game.py
```


## Game Interface

The game uses a simple command-line interface:
- Piles are displayed using candy emojis (🍬)
- Input the pile number and number of candies to take on your turn
- The AI will display its moves after thinking

Example display:
```
🍬🍬🍬🍬🍬
🍬🍬🍬🍬🍬
🍬🍬🍬🍬🍬
🍬🍬🍬🍬🍬
```


## Development Plans

Future enhancements:
- [ ] Implement a graphical user interface
- [ ] Add difficulty levels for AI
- [ ] improve the AI training result
- [ ] Save and load AI training states
- [ ] Add multiplayer support
- [ ] Create mobile app version
- [ ] Have user input the number of piles
- [ ] Have user to choose the last candy is the winning condition or the losing condition

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]