from flask import Flask, jsonify, render_template, request, session
from tictactoe import *
from ai import GameTree
import random
app = Flask(__name__)

AI = GameTree(TicTacToe(3), Player.X)

@app.route('/play')
def make_move():
    game = TicTacToe(3, session['board'])
    xi,xj = (int(request.args['i']), int(request.args['j']))
    game.play_X(xi,xj)
    status = game.status()
    if status:
        return jsonify(status=status)
    i,j = AI.play(Player.O, game)
    game.play_O(i, j)
    status = game.status()
    return jsonify(status=status,
                   x=i, y=j)

@app.route('/')
def index():
    session['board'] = TicTacToe(3).board
    session['user'] = random.randint(1,1000000)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'computer cat'

    app.run(debug=True)
