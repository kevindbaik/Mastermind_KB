class Player:
  def __init__(self, name, id=None, email=None):
    self.name = name
    self.score = 0
    # for API
    self.id = id
    self.email = email

# ------- methods -------
  def make_guess(self, guess):
    return guess

  # ---- getter/setter ------
  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, user_input: str):
    if len(user_input) >= 20:
      raise ValueError("that name is too long!")
    if not user_input.isalpha():
      raise ValueError("your name can only contain letters!")
    self._name = user_input
