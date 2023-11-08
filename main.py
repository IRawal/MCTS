import random

from engine import Engine

engine = Engine(2, 0.2, 2, 1, 3)

while engine.game.get_winner() == 0:
    if engine.game.turn == 1:
        engine.game.make_move(engine.game.turn, random.choice(engine.get_best_moves()))
    else:
        move = int(input("Move: "))
        engine.game.make_move(engine.game.turn, move)
    print(engine.game.board)

