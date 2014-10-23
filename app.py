from flask import Flask, jsonify, render_template, request, session
from tictactoe import *
import random
app = Flask(__name__)

print "created a game board"

@app.route('/play')
def make_move():
    game = Board(3, session['board'])
    game.playX(int(request.args['i']), int(request.args['j']))
    move = game.random_move()
    if move:
        i,j = move
    else:
        # TODO if the computer wins won't notice until next move
        return jsonify(status='done', winner=game.has_winner())
    session['tmp'] = 'foo'
    game.playO(i, j)
    return jsonify(x=i, y=j)

@app.route('/')
def index():
    session['board'] = Board(3).board
    session['user'] = random.randint(1,1000000)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'computer cat'

    app.run(debug=True)
