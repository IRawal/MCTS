class Node:
    def __init__(self, parent, state, bias):
        self.parent = parent
        self.children = []
        self.state = state
        self.bias = bias


class GameState:
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn
