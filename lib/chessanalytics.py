from lib import exceptions, chessmen, chess
import copy


def get_all_positions(board, party):
    boards = []
    for i in range(8):
        for j in range(8):
            for i1 in range(8):
                for j1 in range(8):
                    if((board.get_chessman((i, j)) is not None and board.get_chessman((i, j)).party == party)):
                        try:
                            # DEBUG print(i,j,i1,j1)
                            check_move(board, party, (i, j), (i1, j1))
                        except Exception:
                            continue
                        new_board = copy.deepcopy(board)
                        new_board.relocate((i, j), (i1, j1))
                        boards.append(new_board)
    return boards

def is_check(board, king_party):
    king_pos = board.king_position(king_party)
    current = king_pos
    check = lambda chessman, king_party, figures: ((chessman is not None and chessman.party != king_party) and
        (chessman.name in figures))
    chessman = board.get_first_on_vector(current, (-1, 0))
    if(check(chessman, king_party, ['q', 'r'])):
        return True
    chessman = board.get_first_on_vector(current, (0, 1))
    if(check(chessman, king_party, ['q', 'r'])):
        return True
    chessman = board.get_first_on_vector(current, (1, 0))
    if(check(chessman, king_party, ['q', 'r'])):
        return True
    chessman = board.get_first_on_vector(current, (0, -1))
    if(check(chessman, king_party, ['q', 'r'])):
        return True
    chessman = board.get_first_on_vector(current, (-1, 1))
    if(check(chessman, king_party, ['q', 'b'])):
        return True
    chessman = board.get_first_on_vector(current, (1, 1))
    if(check(chessman, king_party, ['q', 'b'])):
        return True
    chessman = board.get_first_on_vector(current, (-1, -1))
    if(check(chessman, king_party, ['q', 'b'])):
        return True
    chessman = board.get_first_on_vector(current, (1, -1))
    if(check(chessman, king_party, ['q', 'b'])):
        return True
    change = lambda a, b: (a[0] + b[0], a[1] + b[1])
    # (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1) knight-00
    chessman = board.get_chessman(change(current, (2, 1)))
    if(check(chessman, king_party, ['k'])):
        return True
    chessman = board.get_chessman(change(current, (1, 2)))
    if(check(chessman, king_party, ['k'])):
        return True
    chessman = board.get_chessman(change(current, (-1, 2)))
    if(check(chessman, king_party, ['k'])):
        return True
    chessman = board.get_chessman(change(current, (-2, 1)))
    if(check(chessman, king_party, ['k'])):
        return True
    chessman = board.get_chessman(change(current, (-2, -1)))
    if(check(chessman, king_party, ['k'])):
        return True
    chessman = board.get_chessman(change(current, (-1, -2)))
    if(check(chessman, king_party, ['k'])):
        return True
    chessman = board.get_chessman(change(current, (1, -2)))
    if(check(chessman, king_party, ['k'])):
        return True

    chessman = board.get_chessman(change(current, (2, -1)))
    if(check(chessman, king_party, ['k'])):
        return True
    if(king_party == chess.Party.Black):
        chessman = board.get_chessman(change(current, (-1, -1)))
        if(check(chessman, king_party, ['p'])):
            return True
        chessman = board.get_chessman(change(current, (-1, 1)))
        if(check(chessman, king_party, ['p'])):
            return True
    else:
        chessman = board.get_chessman(change(current, (1, -1)))
        if(check(chessman, king_party, ['p'])):
            return True
        chessman = board.get_chessman(change(current, (1, 1)))
        if(check(chessman, king_party, ['p'])):
            return True     
    return False

def is_mate(board, king_party):
    all_boards = get_all_positions(board, king_party)
    for new_board in all_boards:
        if(not is_check(new_board, king_party)):
            return False
    return True        

def is_stalemate(board, current_party):
    if(len(get_all_positions(board, current_party)) == 0):
        return True
    return False

def check_move(board, current_party, place, to):
    if(chess.is_out_of_range(place) or chess.is_out_of_range(to)):
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

    new_board = copy.deepcopy(board)
    new_board.relocate(place, to)

    if(is_check(new_board, current_party)):
        raise exceptions.Check
    
    change = lambda a, b: (a[0] + b[0], a[1] + b[1])
    delta = lambda a, b: (a[0] - b[0], a[1] - b[1])

    if(chessman.name == 'p'):
        for move in chessman.moves:
            if(change(place, move) == to):
                if(move[1] != 0 and target is not None and target.party == chessmen.next_move(current_party)):
                    return 
                elif(move[1] == 0 and target is None):
                    return
                else:
                    raise exceptions.IncorrectMove

    if(chessman.figure_type is chessmen.FigureType.Finite):
        for move in chessman.moves:
            if(change(place, move) == to):
                return
    else:
        diff = delta(place, to)
        direction = None
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
                    direction = vector
                else:
                    continue
            elif(k2 is None):
                if(k1 > 0):
                    direction = vector
                else:
                    continue
            else:
                if(k1 == k2 and k1 > 0):
                    direction = vector
        if(direction is None):
            raise exceptions.IncorrectMove
        else:
            cur = delta(place, direction)
            while cur != to:
                chessman = board.get_chessman(cur)
                if(chessman is not None):
                    raise exceptions.IncorrectMove
                cur = delta(cur, direction)    
            return 
    raise exceptions.IncorrectMove
