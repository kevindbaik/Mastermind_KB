import unittest
from models.game import Game

class TestGame(unittest.TestCase):
  # making sure API returns
  def test_random_api(self):
    game = Game(1)
    self.assertEqual(len(game.answer), 4)
    self.assertNotEqual(game.answer[3], 9)

if __name__ == '__main__':
  unittest.main()
