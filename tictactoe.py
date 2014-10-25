from random import randint
import copy

def enum(**enums):
    return type('Enum', (), enums)

Direction = enum(ROW=1, COL=2, DIAG=3, REV=4)
Player = enum(X=1, O=-1)
Status = enum(TIE='tie', O_WINS='O', X_WINS='X', IN_PROGRESS=None)

class TicTacToe:

    def __init__(self, size, board=None):
        self.size = int(size)
        if board:
            self.board = board
        else:
            self.board = [[0 for i in range(size)] for j in range(size)]

    def play(self, player, x, y):
        if self.is_occupied(x, y):
            raise Exception('That cell is already taken.')
        self.board[x][y] = player

    def play_X(self, x, y):
        self.play(Player.X, x, y)

    def play_O(self, x, y):
        self.play(Player.O, x, y)

    def full(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.is_occupied(i,j):
                    return False
        return True

    def status(self):
        winner = self.find_winner()
        if winner:
            return winner
        else:
            if not self.full():
                return Status.IN_PROGRESS
            return Status.TIE

    def find_winner(self):
        if self.find_occupied_seq(self.size):
            return Status.X_WINS
        elif self.find_occupied_seq(-self.size):
            return Status.O_WINS
        else:
            return None

    # returns the direction and index of a row that sums up to seq
    def find_occupied_seq(self, seq, already_found=set([])):
        for i in range(self.size):
            score = sum(self.board[i])
            if score == seq and Direction.ROW not in already_found:
                return (Direction.ROW, i)
            score = sum([self.board[j][i] for j in range(self.size)])
            if score == seq and Direction.COL not in already_found:
                return (Direction.COL, i)
        score = sum([self.board[j][j] for j in range(self.size)])
        if score == seq and Direction.DIAG not in already_found:
            return (Direction.DIAG, 0)
        score = sum([self.board[self.size-j-1][j] for j in range(self.size)])
        if score == seq:
            return (Direction.REV, 0)
        return None

    def win_or_block(self):
        # win
        seq = self.find_occupied_seq(Player.O*(self.size-1))
        # block win
        seq = seq if seq else self.find_occupied_seq(Player.X*(self.size-1))
        if seq:
            dir, index = seq
            if dir == Direction.DIAG:
                for i in range(self.size):
                    if not self.is_occupied(i,i):
                        return (i,i)
            if dir == Direction.REV:
                for i in range(self.size):
                    if not self.is_occupied(self.size-i-1,i):
                        return (self.size-i-1,i)
            if dir == Direction.ROW:
                for i in range(self.size):
                    if not self.is_occupied(index, i):
                        return (index, i)
            if dir == Direction.COL:
                for i in range(self.size):
                    if not self.is_occupied(i, index):
                        return (i, index)
        return None

    def find_two_way_win(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if not self.is_occupied(i,j):
                    tmp_game = TicTacToe(self.size, copy.deepcopy(self.board))
                    tmp_game.play(player, i,j)
                    seq = tmp_game.find_occupied_seq(player*(self.size-1))
                    if seq:
                        seq2 = tmp_game.find_occupied_seq(player*(self.size-1),
                                                          already_found=set([seq[0]]))
                        if seq2:
                            return (i, j)
        return None

    def play_corner(self, player):
        corners = [(0,0), (self.size-1,self.size-1),
                   (0,self.size-1), (self.size-1,0)]
        for corner in corners:
            x,y = corner
            x_opp = self.size-x-1
            y_opp = self.size-y-1
            if self.board[x][y] == -player and not self.is_occupied(x_opp, y_opp):
                return (x_opp, y_opp)
        for corner in corners:
            x,y = corner
            if not self.is_occupied(x,y):
                return corner

    def play_edge(self):
        edges = [(0,self.size/2), (self.size/2,0),
                 (self.size/2,self.size-1), (self.size-1,self.size/2)]
        for edge in edges:
            x,y = edge
            if not self.is_occupied(x,y):
                return edge

    def is_occupied(self, x, y):
        return self.board[x][y] != 0

    def random_move(self):
        x = -1
        y = -1
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    x = i
                    y = j
        if x < 0:
            return None
        while self.is_occupied(x, y):
            x = randint(0,2)
            y = randint(0,2)
        return (x, y)

    def ai_move(self):
        # win or block win
        win = self.win_or_block()
        if win:
            return win

        # create two way wins
        move = self.find_two_way_win(Player.O)
        if move:
            return move

        # prevent two way wins
        move = self.find_two_way_win(Player.X)
        if move:
            return move

        # play in the center
        if not self.is_occupied(self.size/2, self.size/2):
            return(self.size/2, self.size/2)

        # play in the opposite corner
        corner = self.play_corner(Player.O)
        if corner:
            return corner

        # play an edge
        edge = self.play_edge()
        if edge:
            return edge

        raise Exception('Should have covered all the cases...')

    def __str__(self):
        s = ''
        for row in self.board:
            for cell in row:
                s += str(cell) + ' '
            s += '\n'
        return s
