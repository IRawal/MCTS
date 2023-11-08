import random
import numpy as np

from connect_four import ConnectFourGame
from tree import Node, GameState


# Search every child of every leaf and add to tree
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


# Goes from root to depth of max_depth choosing based on randomness and bias
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


# Play game out from leaf
# min_val = 0 gives 0 or 1 for use in selection weight
# min_val = -1 gives -1 or 1 for use in minimax
def rollout(node, game, player, n, min_val):
    val_sum = 0
    for i in range(0, n):
        game.set_state(node.state)
        while (winner := game.get_winner()) == 0:
            game.make_move(game.turn, random.choice(game.get_legal_moves()))
        val_sum += 1 if winner == player else min_val
    node.bias = val_sum / n


# Start at leaves and add children bias to parent
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


# Updates probabilities for use during selection
# Done in two steps, adds children to parent, second step divides each parent by children to get average
def back_prop(leaves, root):
    add_bias(leaves.copy())
    average_bias(root)


# Prints out leaves
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


class Engine:
    def __init__(self, iterations, initial_probability, selection_depth, search_rollouts, minimax_rollouts, start_board=None, start_turn=1):
        self.iterations = iterations
        self.initial_probability = initial_probability
        self.selection_depth = selection_depth
        self.search_rollouts = search_rollouts
        self.minimax_rollouts = minimax_rollouts
        self.game = ConnectFourGame(6, 7, start_board, start_turn)

    def get_best_moves(self):
        root = Node(None, GameState(self.game.board, self.game.turn), self.initial_probability)
        leaves = []
        # Perform n iteration of MCTS
        for i in range(0, self.iterations):
            selection(root, self.game, 0, self.selection_depth, leaves)
            leaves = get_leaves(root, leaves)
            new_leaves = []
            for leaf in leaves:
                new_leaves += expand_game_tree(leaf, self.game, [])
            for leaf in new_leaves:
                rollout(leaf, self.game, root.state.turn, self.search_rollouts, 0)
            back_prop(new_leaves, root)

        leaves = get_leaves(root, [])
        print(f"Generated tree of with {len(leaves)} nodes")

        # Perform rollouts to get a rough average value of each leaf
        # Used later for minimax
        for leaf in leaves:
            rollout(leaf, self.game, root.state.turn, self.minimax_rollouts, -1)

        max_val = minimax(root, root.state.turn)

        possible_moves = []
        for child in root.children:
            if child.bias != max_val:
                continue
            optimal_move = np.argwhere(child.state.board - root.state.board).flatten()[1]
            possible_moves.append(optimal_move)
        self.game.set_state(root.state)
        # Returns a list of all moves with an optimal outcome (multiple moves have same expected outcome)
        return possible_moves
