import numpy as np
from scipy.ndimage import convolve

from connect_four import ConnectFourGame
from tree import Node, GameState

nodes = 0


def build_game_tree(parent, game, depth, max_depth):
    game.set_state(parent.state)
    legal_moves = game.get_legal_moves()
    for move in legal_moves:
        game.set_state(parent.state)

        game.make_move(game.turn, move)
        node = Node(parent, GameState(game.board, game.turn), 1 / len(legal_moves))
        parent.children.append(node)

        if game.get_winner() != 0 or depth >= max_depth:
            continue
        build_game_tree(node, game, depth + 1, max_depth)


four_game = ConnectFourGame(5, 5)

head = Node(None, GameState(four_game.board, four_game.turn), 1 / len(four_game.get_legal_moves()))

build_game_tree(head, four_game, 1, 7)
