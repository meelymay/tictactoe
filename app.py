from flask import Flask, jsonify, render_template, request
from tictactoe import *
app = Flask(__name__)

game = Board(3)
print "created a game board"

@app.route('/play')
def make_move():
    game.playX(int(request.args['i']), int(request.args['j']))
    move = game.randomMove()
    if move:
        i,j = move
    else:
        return jsonify(winner='done')
    game.playO(i, j)
    return jsonify(x=i, y=j)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
