from models.game import Game
from models.player import Player
from .console import Console

class Controller:
  def __init__(self):
    self.console = Console()

  def run(self):
    self.console.display_header("Working!!")
