from tictactoe import *
import unittest

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        pass

    def test_play(self):
        game = TicTacToe(3)

        self.assertEqual(game.board[0][1], 0)
        self.assertEqual(game.board[1][2], 0)
        self.assertEqual(game.board[2][1], 0)

        game.play_X(0,1)
        game.play_X(1,2)
        game.play_O(2,1)

        self.assertEqual(game.board[0][0], 0)
        self.assertEqual(game.board[0][1], 1)
        self.assertEqual(game.board[1][2], 1)
        self.assertEqual(game.board[2][1], -1)
        self.assertEqual(game.board[2][2], 0)

        self.assertTrue(game.is_occupied(0,1))
        self.assertTrue(game.is_occupied(1,2))
        self.assertTrue(game.is_occupied(2,1))
        self.assertFalse(game.is_occupied(0,0))
        self.assertFalse(game.is_occupied(1,1))

        # should raise an exception if playing in an occupied space
        self.assertRaises(Exception, game.play_O, (0,1))
        self.assertRaises(Exception, game.play_X, (1,2))

        game = TicTacToe(3)
        game.play(Player.X,0,1)
        game.play(Player.X,1,2)
        game.play(Player.O,2,1)

        self.assertEqual(game.board[0][0], 0)
        self.assertEqual(game.board[0][1], 1)
        self.assertEqual(game.board[1][2], 1)
        self.assertEqual(game.board[2][1], -1)

    def test_status(self):
        game = TicTacToe(3)

        self.assertEqual(game.find_winner(), Status.IN_PROGRESS)
        game.play_X(0,0)
        game.play_X(1,1)
        game.play_X(2,2)
        self.assertEqual(game.find_winner(), Status.X_WINS)
        self.assertEqual(game.status(), Status.X_WINS)

        game = TicTacToe(3)
        game.play_O(2,0)
        game.play_O(1,1)
        game.play_O(0,2)
        self.assertEqual(game.find_winner(), Status.O_WINS)
        self.assertEqual(game.status(), Status.O_WINS)

        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(0,1)
        game.play_X(0,2)
        self.assertEqual(game.find_winner(), Status.X_WINS)

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(1,1)
        game.play_X(2,1)
        self.assertEqual(game.find_winner(), Status.X_WINS)

        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_O(0,1)
        game.play_O(0,2)
        game.play_O(1,0)
        game.play_X(1,1)
        game.play_X(1,2)
        game.play_X(2,0)
        game.play_X(2,1)
        game.play_O(2,2)
        self.assertEqual(game.status(), Status.TIE)

    def test_find_seq(self):
        game = TicTacToe(3)
        game.play_O(0,0)
        game.play_O(0,1)
        self.assertEquals(game.find_occupied_seq(-2), (Direction.ROW, 0))

        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(1,0)
        self.assertEquals(game.find_occupied_seq(2), (Direction.COL,0))

        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(1,1)
        self.assertEquals(game.find_occupied_seq(2), (Direction.DIAG, 0))

        game = TicTacToe(3)
        game.play_O(2,0)
        game.play_O(0,2)
        self.assertEquals(game.find_occupied_seq(-2), (Direction.REV, 0))

if __name__ == '__main__':
    unittest.main()
