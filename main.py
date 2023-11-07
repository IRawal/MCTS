import numpy as np
from scipy.ndimage import convolve

from connect_four import ConnectFourGame

game = ConnectFourGame(5, 5)
for i in range(0, 3):
    game.make_move(1, i)
for i in range(0, 3):
    game.make_move(2, i)

game.make_move(2, 0)
game.make_move(2, 3)
game.make_move(2, 0)
game.make_move(2, 0)

for i in range(1, 4):
    game.make_move(1, i)

print(game.board)
print(game.get_winner())
# h_kern = np.ones((1, 4))
# v_kern = np.transpose(h_kern)
# diag1_kernel = np.eye(4)
# diag2_kernel = np.fliplr(diag1_kernel)
#
# kerns = [h_kern, v_kern, diag1_kernel, diag2_kernel]
#
# copy = game.board.copy()
# copy[:][copy == 2] = 0
#
# print(game.board)
#
# for kern in kerns:
#     print(convolve(copy, kern) == 4)
