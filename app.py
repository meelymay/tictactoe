from flask import Flask, jsonify, render_template, request, session
from tictactoe import *
from hard_coded_player import HardCodedPlayer
from player import AIPlayer
from ai import GameTree
import random
app = Flask(__name__)

AI = GameTree(TicTacToe(3), Player.X)

@app.route('/play')
def make_move():
    # create the game and get the clicked position
    game = TicTacToe(3, session['board'])
    xi, xj = (int(request.args['i']), int(request.args['j']))

    # skip if the game is already over
    # or attempting to play in an occupied space
    if session['status'] is not None or game.is_occupied(xi, xj):
        return jsonify(status=session['status'])

    # X plays
    game.play_X(xi, xj)

    # check if the game is over now
    status = game.status()
    if status:
        return jsonify(status=status)

    # the AI player makes a move
    i,j = AI.play(game)
    game.play_O(i, j)

    # return game status and AI move
    return jsonify(status=game.status(),
                   x=i, y=j)

@app.route('/')
def index():
    # initialize a new board
    # session['user'] = random.randint(1, 1000000)
    session['board'] = TicTacToe(3).board
    session['status'] = None
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'computer cat'

    app.run(debug=True)
