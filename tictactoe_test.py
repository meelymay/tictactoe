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

    def test_winners(self):
        game = TicTacToe(3)

        self.assertEqual(game.find_winner(), 0)
        game.play_X(0,0)
        game.play_X(1,1)
        game.play_X(2,2)
        print "\nDIAG"
        self.assertEqual(game.find_winner(), 1)

        game = TicTacToe(3)
        game.play_O(2,0)
        game.play_O(1,1)
        game.play_O(0,2)
        print "\nREV DIAG"
        self.assertEqual(game.find_winner(), -1)

        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(0,1)
        game.play_X(0,2)
        print "\nROW"
        self.assertEqual(game.find_winner(), 1)

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(1,1)
        game.play_X(2,1)
        print "\nCOLUMN"
        self.assertEqual(game.find_winner(), 1)

if __name__ == '__main__':
    unittest.main()
