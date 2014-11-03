from tictactoe import *
from player import AIPlayer

class HardCodedPlayer(AIPlayer):
    def win_or_block(self, game):
        # win
        seq = game.find_occupied_seq(Player.O*(game.size-1))
        # block win
        seq = seq if seq else game.find_occupied_seq(Player.X*(game.size-1))

        if seq:
            # find the empty space in the occupied(2) sequence
            dir, index = seq
            if dir == Direction.DIAG:
                for i in range(game.size):
                    if not game.is_occupied(i,i):
                        return (i,i)
            if dir == Direction.REV:
                for i in range(game.size):
                    if not game.is_occupied(game.size-i-1,i):
                        return (game.size-i-1,i)
            if dir == Direction.ROW:
                for i in range(game.size):
                    if not game.is_occupied(index, i):
                        return (index, i)
            if dir == Direction.COL:
                for i in range(game.size):
                    if not game.is_occupied(i, index):
                        return (i, index)
        return None

    def find_two_way_win(self, player, game):
        for i in range(game.size):
            for j in range(game.size):
                if not game.is_occupied(i,j):
                    # for each potential move, check if there's a two way win
                    tmp_game = TicTacToe(game.size, copy.deepcopy(game.board))
                    tmp_game.play(player, i,j)
                    # find seq in one direction
                    seq = tmp_game.find_occupied_seq(player*(game.size-1))
                    if seq:
                        # check all other directions
                        seq2 = tmp_game.find_occupied_seq(player*(game.size-1),
                                                          already_found=set([seq[0]]))
                        if seq2:
                            return (i, j)
        return None

    def play_corner(self, player, game):
        corners = [(0,0), (game.size-1, game.size-1),
                   (0, game.size-1), (game.size-1,0)]
        for corner in corners:
            x,y = corner
            x_opp = game.size-x-1
            y_opp = game.size-y-1
            # play the corner opposite your opponent
            if game.board[x][y] == -player and not game.is_occupied(x_opp, y_opp):
                return (x_opp, y_opp)
        # otherwise just play an empty corner
        for corner in corners:
            x,y = corner
            if not game.is_occupied(x,y):
                return corner

    def play_edge(self, game):
        edges = [(0, game.size/2), (game.size/2,0),
                 (game.size/2, game.size-1), (game.size-1, game.size/2)]
        # play an empty edge
        for edge in edges:
            x,y = edge
            if not game.is_occupied(x,y):
                return edge

    def play(self, game):
        # win or block win
        win = self.win_or_block(game)
        if win:
            return win

        # create two way wins
        move = self.find_two_way_win(Player.O, game)
        if move:
            return move

        # prevent two way wins
        move = self.find_two_way_win(Player.X, game)
        if move:
            return move

        # play in the center
        if not game.is_occupied(game.size/2, game.size/2):
            return(game.size/2, game.size/2)

        # play in the opposite corner
        corner = self.play_corner(Player.O, game)
        if corner:
            return corner

        # play an edge
        edge = self.play_edge(game)
        if edge:
            return edge

        raise Exception('Should have covered all the cases...')
