from tictactoe import *
from copy import deepcopy
from player import AIPlayer

STATUS_TO_SCORE = {Status.TIE: 0,
                   Status.X_WINS: 100,
                   Status.O_WINS: -100,
                   Status.IN_PROGRESS: None}

class GameTree(AIPlayer):
    def __init__(self, game, player,
                 mini_max=None,
                 depth=0):
        if mini_max is None:
            # initialize the mini_max dictionary for the whole Tree
            mini_max = {Player.X: {}, Player.O: {}}
        if game.status() == Status.IN_PROGRESS:
            children = {}
            for i in range(game.size):
                for j in range(game.size):
                    if game.is_occupied(i,j):
                        continue
                    # create a temporary board for each possible play, recurse
                    tmp_game = TicTacToe(game.size,
                                         deepcopy(game.board))
                    tmp_game.play(player, i, j)
                    # memoization
                    if str(tmp_game) in mini_max[-player]:
                        child = mini_max[-player][str(tmp_game)]
                    else:
                        child = GameTree(tmp_game,
                                         # player switches
                                         -player,
                                         # children inherit parent's mini_max dict
                                         # (to populate it)
                                         mini_max=mini_max,
                                         # one move deeper
                                         depth=depth+1)
                    children[(i,j)] = child
            # choose the move which maximizes player's score (minimizes -player's)
            max_child = max(children, key=lambda x: -children[x].score)
            self.score = -children[max_child].score
            self.next_move = max_child
        else:
            self.score = self.calc_score(game, player, depth)
            self.next_move = None
        mini_max[player][str(game)] = self
        self.mini_max = mini_max

    def calc_score(self, game, player, depth):
        # valued scores for winning/losing
        # mulitply by player to make positive if win, negative if loss
        base_score = STATUS_TO_SCORE[game.status()]*player
        # include depth, we want to win sooner, lose later
        if base_score < 0:
            return depth - 2**(game.size**2)
        elif base_score > 0:
            return 2**(game.size**2) - depth
        else:
            return 0

    # play the move which maximizes score for player (mini_max)
    def play(self, game, player=Player.O):
        mini_max = self.mini_max[player][str(game)]
        return mini_max.next_move

