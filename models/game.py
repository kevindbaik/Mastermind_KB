import requests

class Game:
  def __init__(self, difficulty):
    self.difficulty = difficulty
    self.answer = self._generate_answer()
    self.attempts = 10
    self.history = []
    self.hints = 2

  # ------- methods ----------


  # ------- private methods ----------
  def _generate_answer(self):
    url = f"https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
    response = requests.get(url)

    if response.status_code == 200:
      list_nums = response.text.strip().split()
      answer_string = ''.join(list_nums)
      return answer_string
    else:
      print("Failed to retrieve data...")
      return "9999"
