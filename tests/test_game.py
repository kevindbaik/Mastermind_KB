import unittest
from models.game import Game

class TestGame(unittest.TestCase):
  # check_answer method
  def test_check_answer(self):
    game = Game(1)
    game.answer = "1234"
    user_answer = "1234"
    result = game.check_answer(user_answer)
    self.assertTrue(result)

  def test_check_answer_incorrect(self):
    game = Game(1)
    game.answer = "1234"
    user_answer = "7777"
    result = game.check_answer(user_answer)
    self.assertFalse(result)

  # decrement_attempts method
  def test_decrement(self):
    game = Game(1)
    self.assertTrue(game.attempts, 10)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 9)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 8)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 7)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 6)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 5)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 4)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 3)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 2)
    game.decrement_attempt()
    self.assertTrue(game.attempts, 1)
    game.decrement_attempt()
    self.assertEqual(game.attempts, 0)

  # game_over method
  def test_game_over_win(self):
    game = Game(1)
    game.answer = "1234"
    user_choice = "7777"
    game.check_answer(user_choice)
    game.decrement_attempt()
    user_choice = "1234"
    game.check_answer(user_choice)
    game.end_game_win()
    self.assertTrue(game.win)
    self.assertTrue(game.game_over)

  # give_feedback method
  def test_give_feedback_exact_matches(self):
    game = Game(1)
    game.answer = "1234"
    correct_location, correct_number = game.give_feedback("1234")
    self.assertEqual(correct_location, 4)
    self.assertEqual(correct_number, 4)

  def test_give_feedback_zero_matches(self):
    game = Game(1)
    game.answer = "1234"
    correct_location, correct_number = game.give_feedback("5555")
    self.assertEqual(correct_location, 0)
    self.assertEqual(correct_number, 0)

  def test_give_feedback_only_correct_numbers(self):
    game = Game(1)
    game.answer = "1234"
    correct_location, correct_number = game.give_feedback("4321")
    self.assertEqual(correct_location, 0)
    self.assertEqual(correct_number, 4)

  def test_give_feedback_some_correct_numbers(self):
    game = Game(1)
    game.answer = "1234"
    correct_location, correct_number = game.give_feedback("1536")
    self.assertEqual(correct_location, 2)
    self.assertEqual(correct_number, 2)

  def test_give_feedback_repeated_numbers_one(self):
    game = Game(1)
    game.answer = "1234"
    correct_location, correct_number = game.give_feedback("2222")
    self.assertEqual(correct_location, 1)
    self.assertEqual(correct_number, 1)

  def test_give_feedback_repeated_numbers_two(self):
    game = Game(1)
    game.answer = "2234"
    correct_location, correct_number = game.give_feedback("2222")
    self.assertEqual(correct_location, 2)
    self.assertEqual(correct_number, 2)

  def test_give_feedback_repeated_numbers_three(self):
    game = Game(1)
    game.answer = "1222"
    correct_location, correct_number = game.give_feedback("2222")
    self.assertEqual(correct_location, 3)
    self.assertEqual(correct_number, 3)

  def test_give_feedback_repeated_numbers_four(self):
    game = Game(1)
    game.answer = "2222"
    correct_location, correct_number = game.give_feedback("2222")
    self.assertEqual(correct_location, 4)
    self.assertEqual(correct_number, 4)

  def test_give_feedback_repeated_mixed(self):
    game = Game(1)
    game.answer = "2211"
    correct_location, correct_number = game.give_feedback("1122")
    self.assertEqual(correct_location, 0)
    self.assertEqual(correct_number, 4)

  def test_give_feedback_repeated_outers(self):
    game = Game(1)
    game.answer = "2112"
    correct_location, correct_number = game.give_feedback("1221")
    self.assertEqual(correct_location, 0)
    self.assertEqual(correct_number, 4)

  def test_give_feedback_example_run(self):
    game = Game(1)
    game.answer = "0135"
    correct_location, correct_number = game.give_feedback("2246")
    self.assertEqual(correct_location, 0)
    self.assertEqual(correct_number, 0)

    correct_location, correct_number = game.give_feedback("0246")
    self.assertEqual(correct_location, 1)
    self.assertEqual(correct_number, 1)

    correct_location, correct_number = game.give_feedback("2211")
    self.assertEqual(correct_location, 0)
    self.assertEqual(correct_number, 1)

    correct_location, correct_number = game.give_feedback("0156")
    self.assertEqual(correct_location, 2)
    self.assertEqual(correct_number, 3)

  # store_history method
  def test_store_history(self):
    game = Game(1)
    game.answer = "1234"
    game.store_history("1111")
    self.assertEqual(len(game.history), 1)
    game.store_history("1121")
    self.assertEqual(len(game.history), 2)
    game.store_history("1411")
    self.assertEqual(len(game.history), 3)

  # get_history method
  def test_get_history(self):
    game = Game(1)
    game.store_history("1234")
    game.store_history("2234")
    game.store_history("3234")
    list = game.get_history()
    self.assertEqual(len(list), 3)

  # give_hint method
  def test_give_hint_correct(self):
    game = Game(1)
    game.answer = "1211"
    game.history.append("1211")
    hint = game.give_hint()
    self.assertEqual(game.hints, 1)

  def test_give_hint_no_more_hints(self):
    game = Game(1)
    game.answer = "7777"
    game.history.append("1211")
    hint = game.give_hint()
    self.assertEqual(game.hints, 1)
    hint = game.give_hint()
    self.assertEqual(game.hints, 0)

  # validate_user_answer method
  def test_validate_user_answer(self):
    game = Game(1)
    with self.assertRaisesRegex(ValueError, "your guess must have 4 numbers..."):
      game.validate_user_answer("11111")
    with self.assertRaisesRegex(ValueError, "each number can only be between 0 and 7..."):
      game.validate_user_answer("9991")
    with self.assertRaisesRegex(ValueError, "your guess can only contain numbers..."):
      game.validate_user_answer("KEVN")
    game3 = Game(3)
    with self.assertRaisesRegex(ValueError, "your guess must have 5 numbers..."):
      game3.validate_user_answer("111211")

  # calculate score
  def test_calculate_score_hard(self):
    game = Game(3)
    self.assertEqual(game.calculate_score(), 2000)
    game.decrement_attempt()
    game.decrement_attempt()
    self.assertEqual(game.calculate_score(), 1800)
    game.history.append("1111")
    game.give_hint()
    self.assertEqual(game.calculate_score(), 1600)

  def test_calculate_score_medium(self):
    game = Game(2)
    self.assertEqual(game.calculate_score(), 1800)
    game.decrement_attempt()
    game.decrement_attempt()
    self.assertEqual(game.calculate_score(), 1600)
    game.history.append("1111")
    game.give_hint()
    self.assertEqual(game.calculate_score(), 1400)

  def test_calculate_score_easy(self):
    game = Game(1)
    self.assertEqual(game.calculate_score(), 1400)
    game.decrement_attempt()
    game.decrement_attempt()
    self.assertEqual(game.calculate_score(), 1200)
    game.history.append("1111")
    game.give_hint()
    self.assertEqual(game.calculate_score(), 1000)

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
    self.assertRaisesRegex(ValueError, "your choice must be a number...", lambda: Game(user_choice))

  def test_difficulty_invalid_range(self):
    user_choice = 5
    self.assertRaisesRegex(ValueError, "your choice must be either 1, 2, or 3...", lambda: Game(user_choice))

  # api returns valid answer
  def test_api_random(self):
    easy_game = Game(1)
    self.assertEqual(len(easy_game.answer), 4)

    med_game = Game(2)
    self.assertEqual(len(med_game.answer), 4)

    hard_game = Game(3)
    self.assertEqual(len(hard_game.answer), 5)

if __name__ == '__main__':

  unittest.main()
