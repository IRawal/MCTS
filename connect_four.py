import numpy as np

from tree import GameState


class ConnectFourGame:
    def __init__(self, n, m):
        self.size = (n, m)
        self.board = np.zeros((n, m))
        self.turn = 1

    def make_move(self, player, col):
        if col >= self.size[1] or self.board[0][col] != 0:
            print(self.board)
            legal_moves = self.get_legal_moves()
            raise Exception()
        if self.board[self.size[0] - 1][col] == 0:
            self.board[self.size[0] - 1][col] = player
        else:
            for i in range(0, self.size[0] - 1):
                if self.board[i + 1][col] != 0:
                    self.board[i][col] = player
                    break
        self.turn = 1 if self.turn == 2 else 2

    def get_legal_moves(self):
        return np.argwhere(self.board[:][0] == 0).flatten()

    def get_winner(self):
        for i in range(self.size[0]):
            for j in range(self.size[1] - 3):
                if self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] != 0:
                    return self.board[i][j]

        for i in range(self.size[0] - 3):
            for j in range(self.size[1]):
                if self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] != 0:
                    return self.board[i][j]

        for i in range(self.size[0] - 3):
            for j in range(self.size[1] - 3):
                if self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] != 0:
                    return self.board[i][j]

        for i in range(self.size[0] - 3):
            for j in range(3, self.size[1]):
                if self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] == self.board[i + 3][j - 3] != 0:
                    return self.board[i][j]
        return 0

    def set_state(self, state: GameState):
        self.turn = state.turn
        self.board = state.board.copy()

    def get_state(self):
        return GameState(self.board, self.turn)
