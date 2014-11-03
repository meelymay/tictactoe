from tictactoe import *
from random import randint

# a simple random tic tac toe player
class AIPlayer:
    def play(self, game):
        max_play = game.size - 1
        if game.full():
            # we won't find an empty space, no play
            return None
        x = randint(0, max_play)
        y = randint(0, max_play)
        # keep generating random moves until we find an unoccupied space
        while game.is_occupied(x, y):
            x = randint(0, max_play)
            y = randint(0, max_play)
        return (x, y)

