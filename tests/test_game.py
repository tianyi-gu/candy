import unittest
from src.game.game import CandyGame

class TestCandyGame(unittest.TestCase):
    def test_initial_game_state(self):
        game = CandyGame(num_piles=3)
        self.assertEqual(len(game.piles), 3)
        self.assertTrue(all(1 <= candies <= 10 for candies in game.piles))
    
    def test_valid_move(self):
        game = CandyGame(initial_piles=[3, 4, 5])
        self.assertTrue(game.make_move(0, 2))
        self.assertEqual(game.piles[0], 1)
    
    def test_invalid_move(self):
        game = CandyGame(initial_piles=[3, 4, 5])
        self.assertFalse(game.make_move(0, 4))
        self.assertEqual(game.piles[0], 3)