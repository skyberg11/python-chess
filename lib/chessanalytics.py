from re import L
from lib import exceptions
import copy

def is_check(board, king_party):
    return True

def is_mate(board, king_party):
    return False

def is_stalemate(board, current_party):
    return True

def check_move(board, current_party, place, to):

    if(place[0] < 0 or place[0] > 7 or place[1] < 0 or place[1] > 7):
        raise exceptions.OutOfRange

    if(to[0] < 0 or to[0] > 7 or to[1] < 0 or to[1] > 7):
        raise exceptions.OutOfRange    

    chessman = board.get_chessman(place)
    target = board.get_chessman(to)
    if(chessman.party != current_party):
        raise exceptions.IncorrectFigure

    if(place == to):
        raise exceptions.LazyMove

    if(target != None and target.party == current_party):
        raise exceptions.SelfHarm

    new_board = copy.copy(board)
    new_board.relocate(place, to)
    if(is_check(new_board, current_party)):
        raise exceptions.Check
    
    
    