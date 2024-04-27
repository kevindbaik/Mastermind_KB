import requests
import random
from typing import Dict, List, Tuple


class Game:
  def __init__(self, difficulty, answer=None, attempts=10, history=[], hints=2, win=False, game_over=False,  player_id=None, id=None):
    self.difficulty = difficulty
    if answer is None:
      self.answer = self._generate_answer()
    else:
      self.answer = answer
    self.attempts = attempts
    self.history = history
    self.hints = hints
    self.win = win
    self.game_over = game_over
    self.player_id = player_id
    self.id = id

  # ------- public methods ----------
  def check_answer(self, user_answer: str) -> bool:
    return user_answer == self.answer

  def decrement_attempt(self) -> int:
    self.attempts -= 1
    return self.attempts

  def get_history (self) -> List[str]:
    return self.history

  def store_history(self, user_answer: str) -> List[str]:
    return self.history.append(user_answer)

  def end_game_win(self):
    self.win = True
    self.game_over = True

  def end_game_lose(self):
    self.win = False
    self.game_over = True

  def give_feedback(self, user_answer: str) -> Tuple[int, int]:
    correct_number = 0
    correct_location = 0
    ua_list = list(user_answer)
    ga_list = list(self.answer)

    for i in range(len(ua_list)):
      if ua_list[i] == ga_list[i]:
        correct_location += 1
        correct_number += 1
        ua_list[i] = None
        ga_list[i] = None

    for number in ua_list:
      if number is not None:
        if number in ga_list:
          ga_list.remove(number)
          correct_number += 1

    return (correct_location, correct_number)

  def give_hint(self) -> str:
    if self.hints <= 0:
      raise Exception("you have no more hints...")
    elif len(self.history) == 0:
      raise Exception("you must take a guess first...")
    else:
      self.hints -= 1
      last_answer = self.history[-1]
      random_index = random.randint(0, len(last_answer) - 1)
      if last_answer[random_index] == self.answer[random_index]:
        return self._display_hint_message_correct(last_answer, random_index)
      elif last_answer[random_index] in self.answer:
        return self._display_hint_message_partial(last_answer, random_index)
      else:
        return self._display_hint_incorrect(last_answer, random_index)


  def validate_user_answer(self, user_answer: str) -> bool:
    settings = { 1: (4,7), 2: (4,9), 3: (5,9) }
    total_nums = settings[self.difficulty][0]
    max_range = settings[self.difficulty][1]

    if len(user_answer) != total_nums:
      raise ValueError(f"your guess must have {total_nums} numbers...")
    for number in user_answer:
      if not number.isdigit():
        raise ValueError("your guess can only contain numbers...")
      elif int(number) > max_range:
        raise ValueError(f"each number can only be between 0 and {max_range}...")
    return True

  def calculate_score(self) -> int:
    score = 0
    score += self.attempts * 100
    score += self.difficulty * 200
    score += self.hints * 200
    return score
  # --------- getters/setters ---------
  @property
  def difficulty(self) -> int:
    return self._difficulty

  @difficulty.setter
  def difficulty(self, user_input: int):
    if not isinstance(user_input, int):
      raise ValueError("your choice must be a number...")
    if user_input not in [1, 2, 3]:
      raise ValueError("your choice must be either 1, 2, or 3...")
    self._difficulty = user_input

  # ------- private methods ----------
  def _generate_answer(self) -> str:
    settings = self._generate_difficulty_settings()  # returns (total digits, max number)
    url = f"https://www.random.org/integers/?num={settings[0]}&min=0&max={settings[1]}&col=1&base=10&format=plain&rnd=new"
    response = requests.get(url)
    if response.status_code == 200:
      list_nums = response.text.strip().split()
      answer_string = ''.join(list_nums)
      return answer_string
    else:
      raise ConnectionError("failed to retrieve data...")

  def _generate_difficulty_settings(self) -> Tuple[int, int]:
    match self.difficulty:
      case 1:
        return (4, 7)
      case 2:
        return (4, 9)
      case 3:
        return (5, 9)

  def _display_hint_message_correct(self, last_answer: str, random_index: int) -> str:
    return f"the number {last_answer[random_index]} in position {random_index + 1} is in the correct position..."
  def _display_hint_message_partial(self, last_answer: str, random_index: int) -> str:
    return f"the number {last_answer[random_index]} in position {random_index + 1} is not in the correct position, but is present in the secret code..."
  def _display_hint_incorrect(self, last_answer: str, random_index: int) -> str:
    return f"the number {last_answer[random_index]} in position {random_index + 1} is not in the secret code..."
  def _display_hint_no_hint(self):
    return "you have no more hints..."
  def _display_hint_no_attempt(self):
    return "you must take a guess first..."
