def display_game_state(piles):
    """
    Display the current state of the game with candy emojis.
    
    Args:
        piles: List of integers representing the candy piles
    """
    print("\nCurrent piles:")
    for i, pile in enumerate(piles):
        print(f"Pile {i + 1}: {'🍬' * pile} ({pile})")
    print()