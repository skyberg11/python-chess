from lib.chessmen import Chessmen, Party, FigureType, next_move
from lib import chessanalytics, interface, exceptions
import math
import copy

class Board():
    """Implementation of chess board in python"""
    def __init__(self):
        self.__board = []
        for i in range(8):
            self.__board.append([None] * 8)

    def __fill__(self, pawn, knight, bishop, rook, queen, king, party):
        first_row = 0
        if(party == Party.Black):
            first_row = 7
        for i in range(8):
            self.__board[max(1, first_row - 1)][i] = copy.copy(pawn)
        self.__board[first_row][0] = copy.copy(rook)
        self.__board[first_row][7] = copy.copy(rook)
        self.__board[first_row][1] = copy.copy(knight)
        self.__board[first_row][6] = copy.copy(knight)
        self.__board[first_row][2] = copy.copy(bishop)
        self.__board[first_row][5] = copy.copy(bishop)
        self.__board[first_row][3] = copy.copy(queen)
        self.__board[first_row][4] = copy.copy(king)
    
    def setup(self):
        pawn = Chessmen(Party.White, FigureType.Finite, "p", 1)
        pawn.set_finite_moves((1, 0), (1, 1), (1, -1))

        knight = Chessmen(Party.White, FigureType.Finite, "k", 3)
        knight.set_finite_moves((2, 1), (1, 2), (-1, 2), (-2, 1),
                            (-2, -1), (-1, -2), (1, -2), (2, -1))

        bishop = Chessmen(Party.White, FigureType.VectorStroke, "b", 3)
        bishop.set_vectors((1, -1), (1, 1), (-1, 1), (-1, -1))

        rook = Chessmen(Party.White, FigureType.VectorStroke, "r", 5)
        rook.set_vectors((1, 0), (0, 1), (-1 ,0), (0, -1))

        queen = Chessmen(Party.White, FigureType.VectorStroke, "q", 9)
        queen.set_vectors((1, -1), (1, 1), (-1, 1), (-1, -1),
                            (1, 0), (0, 1), (-1 ,0), (0, -1))

        king = Chessmen(Party.White, FigureType.Finite, "o", math.inf)
        king.set_finite_moves((1, -1), (1, 1), (-1, 1), (-1, -1),
                                (1, 0), (0, 1), (-1 ,0), (0, -1))

        self.__fill__(pawn, knight, bishop, rook, queen, king, Party.White)

        pawn.set_team(Party.Black)
        pawn.set_finite_moves((-1, 0), (-1, 1), (-1, -1))
        knight.set_team(Party.Black)
        bishop.set_team(Party.Black)
        rook.set_team(Party.Black)
        queen.set_team(Party.Black)
        king.set_team(Party.Black)

        self.__fill__(pawn, knight, bishop, rook, queen, king, Party.Black)

    def get_map(self):
        return copy.copy(self.__board)

    def get_pattern(self):
        map = []
        for i in range(8):
            map.append(['*'] * 8)
            for j in range(8):
                if(self.__board[i][j] is not None):
                    map[i][j] = self.__board[i][j].name
        return map

    def print_board(self):
        for i in range(8):
            for j in range(8):
                if(self.__board[i][j] is not None):
                    if(self.__board[i][j].party == Party.White):
                        print("\033[34m{}".format(self.__board[i][j].name), end='')
                    else:
                        print("\033[31m{}".format(self.__board[i][j].name), end='')
                else:
                    print("\033[37m*", end='')
            print('\033[37m\n', end='')

    def get_chessman(self, cell):
        if(is_out_of_range(cell)):
            return None
        return self.__board[cell[0]][cell[1]]

    def relocate(self, target, to):
        self.__board[to[0]][to[1]] = self.__board[target[0]][target[1]]
        self.__board[target[0]][target[1]] = None
        return

    def king_position(self, party):
        for i in range(8):
            for j in range(8):
                if(self.__board[i][j] is not None and self.__board[i][j].name == "o"
                    and self.__board[i][j].party == party):
                    return (i, j)

    def get_first_on_vector(self, place, vector):
        place = (place[0] + vector[0], place[1] + vector[1])
        if(is_out_of_range(place)):
            return None
        if(place is not None):
            return self.get_chessman(place)
        else:
            return self.get_first_on_vector(place, vector)

def is_out_of_range(place):
    return place[0] < 0 or place[0] > 7 or place[1] < 0 or place[1] > 7

def move(board, current_party):
    try:
        print("Your move:")
        place, to = interface.get_move(current_party)
        chessanalytics.check_move(board, current_party, place, to)
    except exceptions.OutOfRange:
        print("Your move is out of range. Try again")
        move(board, current_party)
        return  
    except exceptions.IncorrectMove:
        print("Bad move. Try again")
        move(board, current_party)
        return      
    except exceptions.IncorrectFigure:
        print("It is not your figure. Try again")
        move(board, current_party)
        return  
    except exceptions.LazyMove:
        print("You must move. Try again")
        move(board, current_party)
        return  
    except exceptions.SelfHarm:
        print("Do not eat yourself. Try again")
        move(board, current_party)
        return  
    except exceptions.Check:
        print("Your move is resulting in check.Try again")
        move(board, current_party)
        return
    board.relocate(place, to)    

def start_game(board, current_party=Party.White):
    print("Game has started")
    while(True):
        print("Moves {}".format(current_party))
        board.print_board()
        move(board, current_party)
        if(chessanalytics.is_check(board, next_move(current_party))):
            print("Check.")
        print("Not Check")
        if(chessanalytics.is_mate(board, next_move(current_party))):
            print("Mate.")
            print("Player on {} wins the game".format(current_party))
            return
        print("NotMate")
        if(chessanalytics.is_stalemate(board, current_party)):
            print("Stalemate.")
            print("Player on {} just stalemated the game".format(current_party))
            return
        current_party = next_move(current_party)