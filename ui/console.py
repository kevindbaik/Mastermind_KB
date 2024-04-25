class Console:
  # ------- read methods ----------
  def read_string(self, prompt):
    string = input(prompt)
    return string

  def read_int(self, prompt, max):
    try:
      string = input(prompt)
      number = int(string)
      if number <= 0 or number > max:
        raise ValueError(f"hey that's not a valid choice!")
      return number
    except:
      raise ValueError(f"hey that's not a valid number!")

  # ------- display methods ----------
  def display_header(self, *strings):
    max_length = max(len(string) for string in strings)
    print("")
    print("=" * max_length)
    for string in strings:
        print(string.center(max_length))
    print("=" * max_length)
    print("")

  def display_message(self, string):
    print(string)
    print("")

  def display_error(self, message):
      print(f"Error: {message}")

  def display_difficulty(self, name):
    print("")
    print("===============================")
    print(f"hello {name.lower()}! choose a difficulty: ")
    print("===============================")
    print("")
    print("1 (Easy)")
    print("2 (Medium)")
    print("3 (Hard)")
    print("")

  def display_game_start(self):
    print("")

  def display_welcome(self, message):
    lines = message.split('\n')
    max_length = max(len(line) for line in lines)
    print("+" + "-" * (max_length + 2) + "+")
    for line in lines:
        print("| " + line + " " * (max_length - len(line)) + " |")
    print("+" + "-" * (max_length + 2) + "+")

  def display_menu(self):
    print("")
    print("1 (Play Against Computer)")
    print("2 (Read Rules)")
    print("3 (Exit)")
    print("")

  def display_game(self, game):
    print("=" * 50)
    print(f"difficulty: {game.difficulty}")
    print("")
    print(f"attempts: {game.attempts}")
    print("")
    print(f"hints available (type hint): {game.hints}")
    print("")
    print("previous attempts:")
    for guess in game.get_history():
        feedback = game.give_feedback(guess)
        print(f"guess: {guess} - correct numbers: {feedback['correct_number']}, correct locations: {feedback['correct_location']}")
    print("=" * 50)
