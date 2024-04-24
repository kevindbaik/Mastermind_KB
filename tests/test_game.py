import unittest
from models.game import Game

class TestGame(unittest.TestCase):

  # difficulty validation
  def test_difficulty_valid(self):
    user_choice1 = 1
    game1 = Game(user_choice1)
    self.assertEqual(game1.difficulty, 1)

    user_choice2 = 2
    game2 = Game(user_choice2)
    self.assertEqual(game2.difficulty, 2)

    user_choice3 = 3
    game3 = Game(user_choice3)
    self.assertEqual(game3.difficulty, 3)

  def test_difficulty_invalid_str(self):
    user_choice = "easy"
    self.assertRaisesRegex(ValueError, "Input must be a number", lambda: Game(user_choice))

  def test_difficulty_invalid_range(self):
    user_choice = 5
    self.assertRaisesRegex(ValueError, "Input must be 1,2,or 3", lambda: Game(user_choice))

  # api returns valid answer
  def test_api_random(self):
    easy_game = Game(1)
    self.assertEqual(len(easy_game.answer), 4)

    med_game = Game(2)
    self.assertEqual(len(med_game.answer), 5)

    hard_game = Game(3)
    self.assertEqual(len(hard_game.answer), 6)

if __name__ == '__main__':
  unittest.main()
