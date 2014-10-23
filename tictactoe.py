from random import randint

def enum(**enums):
    return type('Enum', (), enums)

Directions = enum(ROW=1, COL=2, DIAG=3, REV=4)

class TicTacToe:

    def __init__(self, size, board=None):
        self.size = int(size)
        if board:
            self.board = board
        else:
            self.board = [[0 for i in range(size)] for j in range(size)]
        
    def play_X(self, x, y):
        if self.is_occupied(x, y):
            raise Exception('That cell is already taken.')
        self.board[x][y] = 1

    def play_O(self, x, y):
        if self.is_occupied(x, y):
            raise Exception('That cell is already taken.')
        self.board[x][y] = -1

    def is_over(self):
        if self.find_winner() != 0:
            return True
        else:
            for i in range(self.size):
                for j in range(self.size):
                    if not is_occupied(i,j):
                        return False
                    return True

    # returns 1 if X wins, -1 if O wins, 0 otherwise
    def find_winner(self):
        for i in range(self.size):
            score = sum(self.board[i])
            if abs(score) == self.size:
                return score/self.size
            score = sum([self.board[j][i] for j in range(self.size)])
            if abs(score) == self.size:
                return score/self.size
        score = sum([self.board[j][j] for j in range(self.size)])
        if abs(score) == self.size:
            return score/self.size
        score = sum([self.board[self.size-j-1][j] for j in range(self.size)])
        if abs(score) == self.size:
            return score/self.size
        return 0

    def find_occupied_seq(self, seq):
        for i in range(self.size):
            score = sum(self.board[i])
            if abs(score) == seq:
                return (Directions.ROW, i)
            score = sum([self.board[j][i] for j in range(self.size)])
            if abs(score) == seq:
                return (Directions.COL, i)
        score = sum([self.board[j][j] for j in range(self.size)])
        if abs(score) == seq:
            return (Directions.DIAG, 0)
        score = sum([self.board[self.size-j-1][j] for j in range(self.size)])
        if abs(score) == seq:
            return (Directions.REV, 0)
        return None

    def is_occupied(self, x, y):
        return self.board[x][y] != 0

    def random_move(self):
        # TODO this place for checking is inefficient
        if self.find_winner():
            return None
        x = -1
        y = -1
        zeros = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    zeros += 1
                    x = i
                    y = j
        if x < 0:
            return None
        while self.is_occupied(x, y):
            x = randint(0,2)
            y = randint(0,2)
        return (x, y)

    def ai_move(self):
        # complete rows with two of the same piece
        seq = self.find_occupied_seq(2)
        if seq:
            dir, index = seq
            if dir == Directions.DIAG:
                for i in range(self.size):
                    if not self.is_occupied(i,i):
                        return (i,i)
            if dir == Directions.REV:
                for i in range(self.size):
                    if not self.is_occupied(self.size-i-1,i):
                        return (self.size-i-1,i)
            if dir == Directions.ROW:
                for i in range(self.size):
                    if not self.is_occupied(index, i):
                        return (index, i)
            if dir == Directions.COL:
                for i in range(self.size):
                    if not self.is_occupied(i, index):
                        return (i, index)

        # play in the center if its unoccupied
        if not self.is_occupied(self.size/2, self.size/2):
            return(self.size/2, self.size/2)

        # prevent two way wins
        
        return self.random_move()
