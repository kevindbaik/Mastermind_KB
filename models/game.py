import requests
import random

class Game:
  def __init__(self, difficulty):
    self.difficulty = difficulty
    self.answer = self._generate_answer()
    self.attempts = 10
    self.history = []
    self.hints = 2
    self.win = False
    self.game_over = False

  # ------- methods ----------
  def check_answer(self, user_answer):
    if user_answer == self.answer:
      self.win = True
      self.game_over = True
      return True
    else:
      self.store_history(user_answer)
      return False

  def decrement_attempt(self):
    self.attempts -= 1
    if self.attempts == 0:
      self.game_over = True
    return self.attempts

  def give_feedback(self, user_answer):
    correct_number = 0
    correct_location = 0
    checked_numbers = set()

    for i in range(len(user_answer)):
      if user_answer[i] == self.answer[i]:
        correct_location += 1
        correct_number += 1
        checked_numbers.add(user_answer[i])
      elif user_answer[i] in self.answer and not user_answer[i] in checked_numbers:
        correct_number += 1
        checked_numbers.add(user_answer[i])

    feedback = { "correct_location" : correct_location, "correct_number" : correct_number }
    return feedback

  def store_history(self, user_answer):
    return self.history.append(user_answer)

  def get_history (self):
    return self.history

  def give_hint(self):
    if self.hints <= 0:
      return (None, "You have no more hints.")
    if len(self.history) == 0:
      return (None, "You must take a guess first.")

    last_answer = self.history[-1]
    random_index = random.randint(0, len(last_answer) - 1)

    if last_answer[random_index] == self.answer[random_index]:
      message = f"The number {last_answer[random_index]} in position {random_index + 1} is in the correct position."
    elif last_answer[random_index] in self.answer:
      message = f"The number {last_answer[random_index]} in position {random_index + 1} is not in the correct position, but is present in the secret code."
    else:
      message = f"The number {last_answer[random_index]} in position {random_index + 1} is not in the secret code."

    self.hints -= 1
    return (last_answer, message)

  # --------- getters/setters ---------
  @property
  def difficulty(self):
    return self._difficulty

  @difficulty.setter
  def difficulty(self, user_input):
    if not isinstance(user_input, int):
      raise ValueError("Input must be a number")
    if user_input not in [1, 2, 3]:
      raise ValueError("Input must be 1,2,or 3")
    self._difficulty = user_input

  # ------- private methods ----------
  def _generate_answer(self):
    settings = self._generate_difficulty_settings()  # returns (total digits, max number)

    url = f"https://www.random.org/integers/?num={settings[0]}&min=0&max={settings[1]}&col=1&base=10&format=plain&rnd=new"
    response = requests.get(url)

    if response.status_code == 200:
      list_nums = response.text.strip().split()
      answer_string = ''.join(list_nums)
      return answer_string
    else:
      print("Failed to retrieve data...")

  def _generate_difficulty_settings(self):
    match self.difficulty:
      case 1:
        return (4, 7)
      case 2:
        return (4, 9)
      case 3:
        return (5, 9)
