class Player:
  def __init__(self, name, id=None, email=None, password=None):
    self.name = name
    self.id = id
    self.email = email
    self.password = password

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
      raise ValueError("Name must be less than 20 characters")
    if not user_input.isalpha():
      raise ValueError("Name can only contain letters")
    self._name = user_input

  @property
  def email(self) -> str:
    return self._email

  @email.setter
  def email(self, user_input: str):
    if user_input and "@" not in user_input:
      raise ValueError("Invalid email address")
    self._email = user_input

  @property
  def password(self) -> str:
    return self._password

  @password.setter
  def password(self, user_input: str):
    if user_input and len(user_input) < 8:
      raise ValueError("Password must be at least 8 characters long")
    self._password = user_input
