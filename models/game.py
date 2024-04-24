import requests

class Game:
  def __init__(self, difficulty):
    self.difficulty = difficulty
    self.answer = self._generate_answer()
    self.attempts = 10
    self.history = []
    self.hints = 2

  # ------- methods ----------


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
    range = self._generate_max_range()
    url = f"https://www.random.org/integers/?num={range}&min=0&max=7&col=1&base=10&format=plain&rnd=new"
    response = requests.get(url)

    if response.status_code == 200:
      list_nums = response.text.strip().split()
      answer_string = ''.join(list_nums)
      return answer_string
    else:
      print("Failed to retrieve data...")
      return "9999"

  def _generate_max_range(self):
    match self.difficulty:
      case 1:
        return 4
      case 2:
        return 5
      case 3:
        return 6
