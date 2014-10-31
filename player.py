from tictactoe import *
from random import randint

class AIPlayer:
  def play(self, game):
      if game.full():
          return None
      x = randint(0,2)
      y = randint(0,2)
      while game.is_occupied(x, y):
          x = randint(0,2)
          y = randint(0,2)
      return (x, y)


