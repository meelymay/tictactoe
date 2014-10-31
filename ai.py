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
            mini_max = {Player.X: {}, Player.O: {}}
        self.node = game
        self.player = player
        verbose = False not in [game.board[1][0] == 1,
                                game.board[0][1] == 1,
                                game.board[0][2] == 1,
                                game.board[2][1] == 1,
                                game.board[0][0] == -1,
                                game.board[1][1] == -1,
                                game.board[1][2] == -1,
                                game.board[2][0] == -1]

        if game.status() == Status.IN_PROGRESS:
            children = {}
            for i in range(game.size):
                for j in range(game.size):
                    if game.is_occupied(i,j):
                        continue
                    tmp_game = TicTacToe(game.size,
                                         deepcopy(game.board))
                    tmp_game.play(player, i, j)
                    if str(tmp_game) in mini_max[-player]:
                        child = mini_max[-player][str(tmp_game)]
                    else:
                        child = GameTree(tmp_game, -player,
                                         mini_max=mini_max,
                                         depth=depth+1)
                    children[(i,j)] = child
            max_child = max(children, key=lambda x: -children[x].score)
            self.score = -children[max_child].score
            self.next_move = max_child
        else:
            self.score = self.calc_score(game, player, depth)
            self.next_move = None
        mini_max[player][str(game)] = self
        self.mini_max = mini_max

    def calc_score(self, game, player, depth):
        base_score = STATUS_TO_SCORE[game.status()]*player
        if base_score < 0:
            return depth - 2**(game.size**2)
        elif base_score > 0:
            return 2**(game.size**2) - depth
        else:
            return 0

    def play(self, player, game):
        mini_max = self.mini_max[player][str(game)]
        return mini_max.next_move

