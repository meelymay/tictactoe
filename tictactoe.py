from random import randint
import copy

def enum(**enums):
    return type('Enum', (), enums)

Direction = enum(ROW=1, COL=2, DIAG=3, REV=4)
Player = enum(X=1, O=-1)

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

    def find_two_way_win(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if not self.is_occupied(i,j):
                    tmp_game = TicTacToe(self.size, copy.deepcopy(self.board))
                    tmp_game.play_O(i,j)
                    seq = self.find_occupied_seq(player*(self.size-1))
                    if seq:
                        seq = self.find_occupied_seq(player*(self.size-1),
                                                already_found=set(seq[0]))
                        if seq:
                            print "\tfound two way",i,j
                            return (i, j)
        return None

    def is_occupied(self, x, y):
        print "checking occupied",x,y,self.board[x][y]
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
        # win
        seq = self.find_occupied_seq(-(self.size-1))
        # block win
        seq = seq if seq else self.find_occupied_seq(self.size-1)
        if seq:
            dir, index = seq
            if dir == Direction.DIAG:
                for i in range(self.size):
                    if not self.is_occupied(i,i):
                        print "returning diag"
                        return (i,i)
            if dir == Direction.REV:
                for i in range(self.size):
                    if not self.is_occupied(self.size-i-1,i):
                        print "returning rev diag"
                        return (self.size-i-1,i)
            if dir == Direction.ROW:
                for i in range(self.size):
                    if not self.is_occupied(index, i):
                        print "returning row"
                        return (index, i)
            if dir == Direction.COL:
                for i in range(self.size):
                    if not self.is_occupied(i, index):
                        print "returning col"
                        return (i, index)

        # create two way wins
        move = self.find_two_way_win(-1)
        if move:
            print "returning two way"
            return move

        # prevent two way wins
        move = self.find_two_way_win(1)
        if move:
            print "returning block two way"
            return move

        # play in the center
        if not self.is_occupied(self.size/2, self.size/2):
            return(self.size/2, self.size/2)

        # play in the opposite corner

        # play a corner

        # play an edge

        print "returning random move"
        return self.random_move()
