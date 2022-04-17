from lib import chess

board = chess.Board()
board.setup()
chess.start_game(board)
# map = board.get_map()

# for i in range(8):
#     for j in range(8):
#         if(map[i][i] is not None):
#             if(map[i][j].party == chess.Party.White):
#                 print("\033[34m{}".format(map[i][j].name), end='')
#             else:
#                 print("\033[31m{}".format(map[i][j].name), end='')
#         else:
#             print("\033[37m*", end='')
#     print('\n', end='')
