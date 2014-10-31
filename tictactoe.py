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

    def is_occupied(self, x, y):
        return self.board[x][y] != 0

    def __str__(self):
        s = ''
        for row in self.board:
            for cell in row:
                s += str(cell) + ' '
            s += '\n'
        return s
