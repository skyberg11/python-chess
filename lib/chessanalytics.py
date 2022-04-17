from lib import exceptions, chessmen
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
    
    if(chessman is None):
        raise exceptions.IncorrectFigure

    if(chessman.party != current_party):
        raise exceptions.IncorrectFigure

    if(place == to):
        raise exceptions.LazyMove

    if(target is not None and target.party == current_party):
        raise exceptions.SelfHarm

    new_board = copy.copy(board)
    new_board.relocate(place, to)
    if(is_check(new_board, current_party)):
        raise exceptions.Check
    
    change = lambda a, b: (a[0] + b[0], a[1] + b[1])
    delta = lambda a, b: (a[0] - b[0], a[1] - b[1])

    if(chessman.figure_type is chessmen.FigureType.Finite):
        for move in chessman.moves:
            if(change(to, move) == to):
                return
    else:
        diff = delta(place, to)
        for vector in chessman.vectors:
            k1 = None
            k2 = None
            if(vector[0] != 0):
                k1 = diff[0] // vector[0]
            elif(diff[0] != 0):
                continue
            if(vector[1] != 0):
                k2 = diff[1] // vector[1]
            elif(diff[1] != 0):
                continue    
            if(k1 is None):
                if(k2 > 0):
                    return
                else:
                    continue
            elif(k2 is None):
                if(k1 > 0):
                    return
                else:
                    continue
            else:
                if(k1 == k2 and k1 > 0):
                    return
    raise exceptions.IncorrectMove
    