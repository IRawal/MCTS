import random
import sys
import numpy as np
from scipy.ndimage import convolve

from connect_four import ConnectFourGame
from tree import Node, GameState

sys.setrecursionlimit(10000)


def expand_game_tree(parent, game, leaves):
    game.set_state(parent.state)
    legal_moves = game.get_legal_moves()
    for move in legal_moves:
        game.set_state(parent.state)

        game.make_move(game.turn, move)
        node = Node(parent, GameState(game.board, game.turn), parent.bias)
        parent.children.append(node)
        leaves.append(node)
    return leaves


def selection(parent, game, depth, max_depth, leaves):
    game.set_state(parent.state)
    legal_moves = game.get_legal_moves()
    for move in legal_moves:
        if random.random() > parent.bias:
            continue

        game.set_state(parent.state)

        game.make_move(game.turn, move)
        node = Node(parent, GameState(game.board, game.turn), parent.bias)
        if node not in parent.children:
            parent.children.append(node)

        if game.get_winner() != 0 or depth >= max_depth:
            leaves.append(node)
            continue
        selection(node, game, depth + 1, max_depth, leaves)
    return leaves


def rollout(node, game, player, n):
    sum = 0
    for i in range(0, n):
        game.set_state(node.state)
        winner = 0
        while (winner := game.get_winner()) == 0:
            game.make_move(game.turn, random.choice(game.get_legal_moves()))
        sum += 1 if winner == player else 0
    node.bias = sum / n


def add_bias(leaves):
    for leaf in leaves:
        if leaf.parent is None:
            return
        leaf.parent.bias += leaf.bias
        leaves.remove(leaf)
        if leaf.parent not in leaves:
            leaves.append(leaf.parent)
    add_bias(leaves)


def average_bias(root):
    child_ct = len(root.children)
    root.bias /= 1 if child_ct == 0 else child_ct
    for child in root.children:
        average_bias(child)


def back_prop(leaves, root):
    add_bias(leaves.copy())
    average_bias(root)


def test(root):
    if len(root.children) == 0:
        print(root.bias)
        return
    for child in root.children:
        test(child)

four_game = ConnectFourGame(5, 5)

head = Node(None, GameState(four_game.board, four_game.turn), 0.7)

leaves = []

for i in range(0, 2):
    leaves = selection(head, four_game, 1, 4, leaves)

    new_leaves = []
    for leaf in leaves:
        new_leaves += expand_game_tree(leaf, four_game, [])
    for leaf in new_leaves:
        rollout(leaf, four_game, head.state.turn, 3)
    back_prop(new_leaves, head)







