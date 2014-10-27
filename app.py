from flask import Flask, jsonify, render_template, request, session
from tictactoe import *
from ai import GameTree
import random
app = Flask(__name__)

AI = None

@app.route('/play')
def make_move():
    game = TicTacToe(3, session['board'])
    i,j = (int(request.args['i']), int(request.args['j']))
    game.play_X(i,j)
    status = game.status()
    if status:
        return jsonify(status=status)

    i,j = GameTree(game, Player.O).play(Player.O, game)
    # print game
    # i,j = AI.play(Player.O, game)
    print "AI playing",i,j
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

#     AI = GameTree(TicTacToe(3), Player.X)
#     for p in AI.mini_max:
#         print "PLAYER",p,"'s MOVES"
#         for g in AI.mini_max[p]:
#             print g
#             print AI.mini_max[p][g].next_move,AI.mini_max[p][g].score,"\n"

    app.run(debug=True)
