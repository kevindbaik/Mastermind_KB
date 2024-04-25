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

  # ------- public methods ----------
  def check_answer(self, user_answer):
    return user_answer == self.answer

  def decrement_attempt(self):
    self.attempts -= 1
    return self.attempts

  def get_history (self):
    return self.history

  def store_history(self, user_answer):
    return self.history.append(user_answer)

  def end_game_win(self):
    self.win = True
    self.game_over = True

  def end_game_lose(self):
    self.win = False
    self.game_over = True

  def give_feedback(self, user_answer):
    correct_number = 0
    correct_location = 0
    ua_list = list(user_answer)
    ga_list = list(self.answer)

    for i in range(len(ua_list)):
      if ua_list[i] == self.answer[i]:
        correct_location += 1
        correct_number += 1
        ua_list[i] = None
        ga_list[i] = None

    for number in ua_list:
      if number is not None:
        if number in ga_list:
          ga_list.remove(number)
          correct_number += 1

    feedback = { "correct_location" : correct_location, "correct_number" : correct_number }
    return feedback

  def give_hint(self):
    if self.hints <= 0:
      hint = "you have no more hints!"
    elif len(self.history) == 0:
      hint = "you must take a guess first!"
    else:
      last_answer = self.history[-1]
      random_index = random.randint(0, len(last_answer) - 1)
      if last_answer[random_index] == self.answer[random_index]:
        hint = self._display_hint_message_correct(last_answer, random_index)
      elif last_answer[random_index] in self.answer:
        hint = self._display_hint_message_partial(last_answer, random_index)
      else:
        hint = self._display_hint_incorrect(last_answer, random_index)
      self.hints -= 1
    print(f"hints remaining: {self.hints}")
    print(hint)


  def validate_user_answer(self, user_answer):
    settings = { 1: (4,7), 2: (4,9), 3: (5,9) }
    total_nums = settings[self.difficulty][0]
    max_range = settings[self.difficulty][1]

    if len(user_answer) != total_nums:
      raise ValueError(f"guess must be {total_nums} numbers!")
    for number in user_answer:
      if not number.isdigit():
        raise ValueError("guess can only contain numbers.")
      elif int(number) > max_range:
        raise ValueError(f"each number can only be between 0 and {max_range}!")
    return True

  # --------- getters/setters ---------
  @property
  def difficulty(self):
    return self._difficulty

  @difficulty.setter
  def difficulty(self, user_input):
    if not isinstance(user_input, int):
      raise ValueError("Input must be a number")
    if user_input not in [1, 2, 3]:
      raise ValueError("Input must be 1, 2, or 3")
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
      raise ConnectionError("Failed to retrieve data...")

  def _generate_difficulty_settings(self):
    match self.difficulty:
      case 1:
        return (4, 7)
      case 2:
        return (4, 9)
      case 3:
        return (5, 9)

  def _display_hint_message_correct(self, last_answer, random_index):
    return f"the number {last_answer[random_index]} in position {random_index + 1} is in the correct position!"
  def _display_hint_message_partial(self, last_answer, random_index):
    return f"the number {last_answer[random_index]} in position {random_index + 1} is not in the correct position, but is present in the secret code!"
  def _display_hint_incorrect(self, last_answer, random_index):
    return f"the number {last_answer[random_index]} in position {random_index + 1} is not in the secret code!"
