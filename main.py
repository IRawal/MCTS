import random

from engine import Engine

engine = Engine(iterations=2, initial_probability=0.4, selection_depth=2, search_rollouts=2, minimax_rollouts=3)

while engine.game.get_winner() == 0:
    if engine.game.turn == 1:
        engine.game.make_move(engine.game.turn, random.choice(engine.get_best_moves()))
    else:
        move = int(input("Move: "))
        engine.game.make_move(engine.game.turn, move)
    print(engine.game.board)

print(f"{engine.game.get_winner()} wins!")
