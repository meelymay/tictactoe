from flask import Flask, jsonify, render_template, request, session
from tictactoe import *
import random
app = Flask(__name__)

@app.route('/play')
def make_move():
    game = TicTacToe(3, session['board'])
    game.play_X(int(request.args['i']), int(request.args['j']))
    move = game.ai_move()
    print "ai move",move
    if move:
        i,j = move
    else:
        # TODO if the computer wins won't notice until next move
        return jsonify(status='done', winner=game.find_winner())
    game.play_O(i, j)
    return jsonify(x=i, y=j)

@app.route('/')
def index():
    session['board'] = TicTacToe(3).board
    session['user'] = random.randint(1,1000000)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'computer cat'

    app.run(debug=True)
