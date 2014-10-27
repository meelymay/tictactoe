from tictactoe import *
from ai import *
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

    def test_ai(self):
        for i in range(5):
            game = TicTacToe(3)
            while game.status() == Status.IN_PROGRESS:
                x,y = game.random_move()
                game.play_X(x,y)
                if game.status() == Status.IN_PROGRESS:
                    x,y = game.ai_move()
                    game.play_O(x,y)
            status = game.status()
            self.assertTrue(status in (Status.TIE, Status.O_WINS))

        game = TicTacToe(3)
        while game.status() == Status.IN_PROGRESS:
            x,y = game.ai_move()
            game.play_X(x,y)
            if game.status() == Status.IN_PROGRESS:
                x,y = game.ai_move()
                game.play_O(x,y)
        status = game.status()
        self.assertEquals(status, Status.TIE)

    def test_win_block(self):
        # block X in top row
        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(0,1)
        self.assertEquals(game.win_or_block(), (0,2))

        # win in top row
        game = TicTacToe(3)
        game.play_O(0,0)
        game.play_O(0,1)
        game.play_O(1,0)
        game.play_O(1,1)
        self.assertEquals(game.win_or_block(), (0,2))

        # win diag
        game = TicTacToe(3)
        game.play_O(0,0)
        game.play_O(2,2)
        self.assertEquals(game.win_or_block(), (1,1))

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

    def test_find_two_seq(self):
        game = TicTacToe(3)
        game.play_O(0,1)
        game.play_O(1,0)
        self.assertEquals(game.find_two_way_win(Player.O), (0,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(1,0)
        self.assertEquals(game.find_two_way_win(Player.X), (0,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(1,0)
        self.assertEquals(game.find_two_way_win(Player.O), None)

    def test_play_positions(self):
        game = TicTacToe(3)
        game.play_X(0,2)
        self.assertEquals(game.play_corner(Player.O), (2,0))

        corners = [(0,0), (0,2), (2,0), (2,2)]
        game = TicTacToe(3)
        self.assertTrue(game.play_corner(Player.O) in corners)

        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(0,2)
        game.play_X(2,2)
        self.assertEquals(game.play_corner(Player.O), (2,0))

        edges = [(0,1), (1,2), (2,1), (1,0)]
        game = TicTacToe(3)
        self.assertTrue(game.play_edge() in edges)

        game = TicTacToe(3)
        self.assertEquals(game.ai_move(), (1,1))

    def test_tree_ai(self):
        game = TicTacToe(3)
        game.play_O(0,1)
        game.play_O(0,2)
        game.play_O(2,1)
        game.play_O(2,2)
        game.play_X(0,0)
        game.play_X(1,1)
        game.play_X(1,2)
        game.play_X(2,0)
        self.assertEqual(GameAI().move(Player.X, game), (1,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(0,2)
        game.play_X(2,1)
        game.play_X(2,2)
        game.play_O(0,0)
        game.play_O(1,1)
        game.play_O(1,2)
        game.play_O(2,0)
        self.assertEqual(GameAI().move(Player.O, game), (1,0))

        game = TicTacToe(3)
        game.play_O(0,1)
        game.play_O(0,2)
        game.play_O(2,1)
        game.play_X(0,0)
        game.play_X(1,1)
        game.play_X(1,2)
        game.play_X(2,0)
        self.assertEqual(GameAI().move(Player.O, game), (1,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(0,2)
        self.assertEqual(GameAI().move(Player.O, game), (0,0))

        game = TicTacToe(3)
        game.play_O(0,1)
        game.play_O(0,2)
        self.assertEqual(GameAI().move(Player.O, game), (0,0))

        print "\n\nDIAGONAL O O"
        game = TicTacToe(3)
        game.play_O(0,0)
        game.play_O(1,1)
        self.assertEqual(GameAI().move(Player.X, game), (2,2))

        print "\n\nDIAGONAL X X"
        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(1,1)
        self.assertEqual(GameAI().move(Player.X, game), (2,2))

    def test_game_tree(self):
        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(1,1)
        tree = GameTree(game, Player.O, None)
        print "tree complete"
        self.assertEqual(tree.play(Player.O, game), (2,2))
        
        game = TicTacToe(3)
        game.play_O(0,0)
        game.play_O(1,1)
        tree = GameTree(game, Player.X, None)
        self.assertEqual(tree.play(Player.X, game), (2,2))

        game = TicTacToe(3)
        game.play_O(0,1)
        game.play_O(0,2)
        game.play_O(2,1)
        game.play_O(2,2)
        game.play_X(0,0)
        game.play_X(1,1)
        game.play_X(1,2)
        game.play_X(2,0)
        tree = GameTree(game, Player.X, None)
        self.assertEqual(tree.play(Player.X, game), (1,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(0,2)
        game.play_X(2,1)
        game.play_X(2,2)
        game.play_O(0,0)
        game.play_O(1,1)
        game.play_O(1,2)
        game.play_O(2,0)
        tree = GameTree(game, Player.O, None)
        self.assertEqual(tree.play(Player.O, game), (1,0))

        game = TicTacToe(3)
        game.play_O(0,1)
        game.play_O(0,2)
        game.play_O(2,1)
        game.play_X(0,0)
        game.play_X(1,1)
        game.play_X(1,2)
        game.play_X(2,0)
        tree = GameTree(game, Player.O, None)
        self.assertEqual(tree.play(Player.O, game), (1,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(0,2)
        tree = GameTree(game, Player.O, None)
        self.assertEqual(tree.play(Player.O, game), (0,0))

if __name__ == '__main__':
    unittest.main()
