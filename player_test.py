from tictactoe import *
from ai import *
from player import *
from hard_coded_player import *
import unittest

class TestPlayers(unittest.TestCase):

    def test_ai(self):
        hard_coded = HardCodedPlayer()
        random_player = AIPlayer()
        for i in range(5):
            game = TicTacToe(3)
            while game.status() == Status.IN_PROGRESS:
                x,y = random_player.play(game)
                game.play_X(x,y)
                if game.status() == Status.IN_PROGRESS:
                    x,y = hard_coded.play(game)
                    game.play_O(x,y)
            status = game.status()
            self.assertTrue(status in (Status.TIE, Status.O_WINS))

        game = TicTacToe(3)
        while game.status() == Status.IN_PROGRESS:
            x,y = hard_coded.play(game)
            game.play_X(x,y)
            if game.status() == Status.IN_PROGRESS:
                x,y = hard_coded.play(game)
                game.play_O(x,y)
        status = game.status()
        self.assertEquals(status, Status.TIE)

    def test_win_block(self):
        player = HardCodedPlayer()

        # block X in top row
        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(0,1)
        self.assertEquals(player.win_or_block(game), (0,2))

        # win in top row
        game = TicTacToe(3)
        game.play_O(0,0)
        game.play_O(0,1)
        game.play_O(1,0)
        game.play_O(1,1)
        self.assertEquals(player.win_or_block(game), (0,2))

        # win diag
        game = TicTacToe(3)
        game.play_O(0,0)
        game.play_O(2,2)
        self.assertEquals(player.win_or_block(game), (1,1))

    def test_find_two_seq(self):
        player = HardCodedPlayer()

        game = TicTacToe(3)
        game.play_O(0,1)
        game.play_O(1,0)
        self.assertEquals(player.find_two_way_win(Player.O, game), (0,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(1,0)
        self.assertEquals(player.find_two_way_win(Player.X, game), (0,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(1,0)
        self.assertEquals(player.find_two_way_win(Player.O, game), None)

    def test_play_positions(self):
        player = HardCodedPlayer()

        game = TicTacToe(3)
        game.play_X(0,2)
        self.assertEquals(player.play_corner(Player.O, game), (2,0))

        corners = [(0,0), (0,2), (2,0), (2,2)]
        game = TicTacToe(3)
        self.assertTrue(player.play_corner(Player.O, game) in corners)

        game = TicTacToe(3)
        game.play_X(0,0)
        game.play_X(0,2)
        game.play_X(2,2)
        self.assertEquals(player.play_corner(Player.O, game), (2,0))

        edges = [(0,1), (1,2), (2,1), (1,0)]
        game = TicTacToe(3)
        self.assertTrue(player.play_edge(game) in edges)

        game = TicTacToe(3)
        self.assertEquals(player.play(game), (1,1))

    def test_game_tree(self):
        game = TicTacToe(3)
        tree = GameTree(game, Player.X, None)

        game = TicTacToe(3)
        game.play_X(0,2)
        game.play_O(0,1)
        game.play_X(1,1)
        self.assertEqual(tree.play(Player.O, game), (2,0))
        
        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(1,0)
        game.play_O(0,0)
        game.play_O(1,1)
        self.assertEqual(tree.play(Player.X, game), (2,2))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_X(0,2)
        game.play_X(2,1)
        game.play_X(2,2)
        game.play_O(0,0)
        game.play_O(1,1)
        game.play_O(1,2)
        game.play_O(2,0)
        self.assertEqual(tree.play(Player.X, game), (1,0))

        game = TicTacToe(3)
        game.play_O(0,1)
        game.play_O(0,2)
        game.play_O(2,1)
        game.play_X(0,0)
        game.play_X(1,1)
        game.play_X(1,2)
        game.play_X(2,0)
        self.assertEqual(tree.play(Player.O, game), (1,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_O(1,1)
        game.play_X(0,2)
        self.assertEqual(tree.play(Player.O, game), (0,0))

        game = TicTacToe(3)
        game.play_X(0,1)
        game.play_O(1,1)
        game.play_X(0,2)
        self.assertEqual(tree.play(Player.O, game), (0,0))

if __name__ == '__main__':
    unittest.main()
