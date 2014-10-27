from tictactoe import *
from copy import deepcopy

STATUS_TO_SCORE = {Status.TIE: 0,
                   Status.X_WINS: 100,
                   Status.O_WINS: -100,
                   Status.IN_PROGRESS: None}

MINI_MAX = {Player.X: {}, Player.O: {}}

class GameTree:
    def __init__(self, game, player, move, depth=0):
        self.node = game
        self.player = player
        self.children = []
        self.move = move
        if game.status() == Status.IN_PROGRESS:
            for i in range(game.size):
                for j in range(game.size):
                    if game.is_occupied(i,j):
                        continue
                    tmp_game = TicTacToe(game.size,
                                         deepcopy(game.board))
                    tmp_game.play(player, i, j)
                    if str(tmp_game) in MINI_MAX[-player]:
                        child = MINI_MAX[-player][str(tmp_game)]
                    else:
                        child = GameTree(tmp_game, -player, (i,j), depth=depth+1)
                    self.children.append(child)
            max_child = max(self.children, key=lambda x: -x.score)
            print "\n\nCHOOSING MOVE FOR",player,"IN\n",game,'\n'
            for child in self.children:
                print child.node,
                print child.score,'\n'
            self.score = -max_child.score
            self.next_move = max_child.move
        else:
            self.score = self.calc_score(game, player, depth)
        MINI_MAX[player][str(game)] = self

    def calc_score(self, game, player, depth):
        base_score = STATUS_TO_SCORE[game.status()]*player
        if base_score < 0:
            return depth - 100
        elif base_score > 0:
            return 100 - depth
        else:
            return 0

    def play(self, player, game):
        mini_max = MINI_MAX[player][str(game)]
        return mini_max.next_move

class GameAI:

    def __init__(self):
        self.memo = {Player.X: {}, Player.O: {}}

    def score(self, player, game):
        # if str(game) in self.memo[player]:
        # return self.memo[player][str(game)]
        if game.find_occupied_seq(player*game.size):
            return 1
        if game.find_occupied_seq(-player*game.size):
            return -1
        else:
            if game.full():
                return 0
            else:
                return None

    def go_deeper(self, game):
        for i in range(game.size):
            for j in range(game.size):
                if game.is_occupied(i,j):
                    continue
                tmp_game = TicTacToe(game.size,
                                     copy.deepcopy(game.board))
                tmp_game.play(player, i, j)
                score = self.score(player, tmp_game)
                # self.memo[player][str(tmp_game)] = score
                if score > max_score:
                    x = i
                    y = j
                    max_score = score

    def move(self, player, game):
        if str(game) in self.memo[player]:
            return self.memo[player][str(game)]
        x = None
        y = None
        max_score = None
        to_explore = [(game, [])]
        while True:
            game, moves = to_explore.pop()
            for i in range(game.size):
                for j in range(game.size):
                    if game.is_occupied(i,j):
                        continue
                    tmp_game = TicTacToe(game.size,
                                         copy.deepcopy(game.board))
                    tmp_game.play(player, i, j)
                    score = self.score(player, tmp_game)
                    if score in [0, 1]:
                        return moves[0]
                    
            player = -player
