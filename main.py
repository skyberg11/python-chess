from lib import chess
from lib import interface
import sys

print("Welcome to the Chess game!.")
print("Type \"new_game\" to start a new game")
print("Type \"load [savename.save]\" to load a save")
print("Type \"savelist\" to see all saves")

while True:
    s = input().split()
    if(s[0] == "new_game"):
        board = chess.Board()
        board.setup()
        chess.start_game(board)
    elif(s[0] == 'load'):
        save = chess.Save.get_save(s[1])
        chess.start_game(save.board, save.party)
    else:
        for save in chess.Save.get_all_saves():
            print(save) 
