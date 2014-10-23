from random import randint

class TicTacToe:
    def __init__(self, size, board=None):
        self.size = size
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

    # returns 1 if X wins, -1 if O wins, 0 otherwise
    def find_winner(self):
        for i in range(self.size):
            print "row",self.board[i]
            score = sum(self.board[i])
            if abs(score) == self.size:
                return score/abs(self.size)
            score = sum([self.board[j][i] for j in range(self.size)])
            print "column",[self.board[j][i] for j in range(self.size)]
            if abs(score) == self.size:
                return score/abs(self.size)
        print "diag",[self.board[j][j] for j in range(self.size)]
        score = sum([self.board[j][j] for j in range(self.size)])
        if abs(score) == self.size:
            return score/abs(self.size)
        print "revdiag",[self.board[self.size-j-1][j] for j in range(self.size)]
        score = sum([self.board[self.size-j-1][j] for j in range(self.size)])
        if abs(score) == self.size:
            return score/abs(self.size)
        return 0

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
