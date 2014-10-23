from random import randint

class Board:
    def __init__(self, size, board=None):
        self.size = size
        if board:
            self.board = board
        else:
            self.board = [[0 for i in range(size)] for j in range(size)]
        
    def playX(self, x, y):
        if self.is_occupied(x, y):
            raise Exception('That cell is already taken.')
        self.board[x][y] = 1

    def playO(self, x, y):
        if self.is_occupied(x, y):
            raise Exception('That cell is already taken.')
        self.board[x][y] = -1

    # returns 1 if X wins, -1 if O wins, 0 otherwise
    def has_winner(self):
        for i in range(self.size):
            score = sum(self.board[i])
            if abs(score) == self.size:
                return score/abs(self.size)
            score = sum([self.board[i][j] for j in range(self.size)])
            if abs(score) == self.size:
                return score/abs(self.size)
        score = sum([self.board[j][j] for j in range(self.size)])
        if abs(score) == self.size:
            return score/abs(self.size)
        score = sum([self.board[self.size-j-1][j] for j in range(self.size)])
        if abs(score) == self.size:
            return score/abs(self.size)
        return 0

    def is_occupied(self, x, y):
        return self.board[x][y] != 0

    def random_move(self):
        # TODO this place for checking is inefficient
        if self.has_winner():
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
