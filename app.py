from flask import Flask, jsonify, render_template, request, session
from tictactoe import *
from ai import GameAI
import random
app = Flask(__name__)

@app.route('/play')
def make_move():
    game = TicTacToe(3, session['board'])
    game.play_X(int(request.args['i']), int(request.args['j']))
    status = game.status()
    if status:
        return jsonify(status=status)

    i,j = GameAI().move(Player.O, game)
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
