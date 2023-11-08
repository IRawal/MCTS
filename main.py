import random
import sys
import numpy as np

from connect_four import ConnectFourGame
from tree import Node, GameState


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


def rollout(node, game, player, n, min):
    sum = 0
    for i in range(0, n):
        game.set_state(node.state)
        while (winner := game.get_winner()) == 0:
            game.make_move(game.turn, random.choice(game.get_legal_moves()))
        sum += 1 if winner == player else min
    node.bias = sum / n


def add_bias(leaves):
    if len(leaves) == 0:
        return
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


def get_leaves(node, leaves):
    if len(node.children) == 0:
        leaves.append(node)
    else:
        for child in node.children:
            get_leaves(child, leaves)
    return leaves


def minimax(root, maximizing_player):
    if len(root.children) == 0:
        return root.bias
    if root.state.turn == maximizing_player:
        root.bias = max(minimax(child, maximizing_player) for child in root.children)
    else:
        root.bias = min(minimax(child, maximizing_player) for child in root.children)
    return root.bias


iterations = 2
initial_probability = 0.2
selection_depth = 2
search_rollouts = 1

minimax_rollouts = 3

four_game = ConnectFourGame(6, 7)

head = Node(None, GameState(four_game.board, four_game.turn), initial_probability)

leaves = []

for i in range(0, iterations):
    selection(head, four_game, 0, selection_depth, leaves)
    leaves = get_leaves(head, leaves)
    new_leaves = []
    for leaf in leaves:
        new_leaves += expand_game_tree(leaf, four_game, [])
    for leaf in new_leaves:
        rollout(leaf, four_game, head.state.turn, search_rollouts, 0)
    back_prop(new_leaves, head)

leaves = get_leaves(head, [])
print(f"Generated tree of with {len(leaves)} nodes")
for leaf in leaves:
    rollout(leaf, four_game, head.state.turn, minimax_rollouts, -1)

max_val = minimax(head, head.state.turn)
possible_moves = []
for child in head.children:
    if child.bias != max_val:
        continue
    optimal_move = np.argwhere(child.state.board - head.state.board).flatten()[1]
    possible_moves.append(optimal_move)

print(f"Optimal: {possible_moves}")
