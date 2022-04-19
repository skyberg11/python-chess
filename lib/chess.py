from lib.chessmen import Chessmen, Party, FigureType, next_move
from PyQt5 import QtCore, QtGui, QtWidgets
from lib import chessanalytics, interface, exceptions
from prettytable import PrettyTable
import math
import copy
import sys
import os



class Save():
    def __init__(self, board, name, party):
        self.board = board
        self.name = name
        self.party = party

    def get_save(dir):
        party = None
        lines = []
        dir = os.path.join(os.getcwd() + "/saves", dir)
        with open(dir, 'r') as f:
            lines = f.readlines()
        name = lines[0]
        if(lines[1] == '1'):
            party = Party.White
        else:
            party = Party.Black
        board = Board()
        for i in range(2, len(lines)):
            l = lines[i].split()
            if(len(l) <= 3):
                continue
            chessman = Board.get_figure(l[3], int(l[2]))
            chessman.moved = bool(l[4])
            board._Board__board[int(l[0])][int(l[1])] = copy.copy(chessman)
        return Save(board, name, party)

    def get_all_saves():
        saves = []
        path = os.getcwd() + "/saves"
        for root, dirs, files in os.walk(path):
            for file in files:
                saves.append(file)
        return saves


class Board():
    """Implementation of chess board in python"""

    def __init__(self):
        self.__board = []
        for i in range(8):
            self.__board.append([None] * 8)

    def get_figure(name, team):
        figure = None
        if(name == 'p'):
            figure = Chessmen(Party.White, FigureType.Finite, "p", 1)
            if(team == Party.White):
                figure.set_finite_moves((1, 0), (1, 1), (1, -1), (2, 0))
            else:
                figure.set_team(Party.Black)
                figure.set_finite_moves((-1, 0), (-1, 1), (-1, -1), (-2, 0))
        if(name == 'n'):
            figure = Chessmen(Party.White, FigureType.Finite, "n", 3)
            figure.set_finite_moves((2, 1), (1, 2), (-1, 2), (-2, 1),
                                    (-2, -1), (-1, -2), (1, -2), (2, -1))
        if(name == 'b'):
            figure = Chessmen(Party.White, FigureType.VectorStroke, "b", 3)
            figure.set_vectors((1, -1), (1, 1), (-1, 1), (-1, -1))
        if(name == 'r'):
            figure = Chessmen(Party.White, FigureType.VectorStroke, "r", 5)
            figure.set_vectors((1, 0), (0, 1), (-1, 0), (0, -1))
        if(name == 'q'):
            figure = Chessmen(Party.White, FigureType.VectorStroke, "q", 9)
            figure.set_vectors((1, -1), (1, 1), (-1, 1), (-1, -1),
                               (1, 0), (0, 1), (-1, 0), (0, -1))
        if(name == 'k'):
            figure = Chessmen(Party.White, FigureType.Finite, "k", math.inf)
            figure.set_finite_moves((1, -1), (1, 1), (-1, 1), (-1, -1),
                                    (1, 0), (0, 1), (-1, 0), (0, -1))
        if(team == Party.Black):
            figure.set_team(Party.Black)
        return figure

    def __fill__(self, party):
        pawn = Board.get_figure('p', party)
        rook = Board.get_figure('r', party)
        queen = Board.get_figure('q', party)
        knight = Board.get_figure('n', party)
        king = Board.get_figure('k', party)
        bishop = Board.get_figure('b', party)
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
        self.__fill__(Party.White)
        self.__fill__(Party.Black)

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
        table = PrettyTable(['X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
        for i in range(8):
            row = []
            row.append(str(i + 1))
            for j in range(8):
                if(self.__board[i][j] is not None):
                    if(self.__board[i][j].party == Party.White):
                        row.append(
                            "\033[34m" + str(self.__board[i][j].name + "\033[37m"))
                    else:
                        row.append(
                            "\033[31m" + str(self.__board[i][j].name + "\033[37m"))
                else:
                    row.append("\033[37m" + ".")
            table.add_row(row)
        print(table)

    def get_chessman(self, cell):
        if(is_out_of_range(cell)):
            return None
        return self.__board[cell[0]][cell[1]]

    def relocate(self, target, to):
        if(self.__board[target[0]][target[1]].moved == False):
            self.__board[target[0]][target[1]].moved = True
            if(self.__board[target[0]][target[1]].name == 'p'):
                self.__board[target[0]][target[1]
                                        ].moves = self.__board[target[0]][target[1]].moves[:-1]
        self.__board[to[0]][to[1]] = self.__board[target[0]][target[1]]
        self.__board[target[0]][target[1]] = None
        return

    def king_position(self, party):
        for i in range(8):
            for j in range(8):
                if(self.__board[i][j] is not None and self.__board[i][j].name == "k"
                        and self.__board[i][j].party == party):
                    return (i, j)

    def get_first_on_vector(self, place, vector):
        place = (place[0] + vector[0], place[1] + vector[1])
        if(is_out_of_range(place)):
            return None
        if(self.get_chessman(place) is not None):
            return self.get_chessman(place)
        else:
            return self.get_first_on_vector(place, vector)


def is_out_of_range(place):
    return place[0] < 0 or place[0] > 7 or place[1] < 0 or place[1] > 7


def move(board, current_party):
    try:
        print("Your move (type help for more information):")
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
    except exceptions.Surrender:
        raise exceptions.Surrender
    except exceptions.Save:
        print("Enter the name of the save:")
        line = input()
        original_stdout = sys.stdout
        path = os.getcwd()
        with open(os.path.join(path, os.path.join("saves", line + ".save")), 'w') as f:
            sys.stdout = f
            print(line)
            print(int(current_party))
            for i in range(8):
                for j in range(8):
                    temp = board.get_chessman((i, j))
                    if(temp is not None):
                        print(str(i), str(j), str(int(temp.party)),
                              str(temp.name), str(temp.moved))
                    else:
                        print(str(i), str(j), "None")
            sys.stdout = original_stdout
        move(board, current_party)
        return
    except exceptions.Board:
        board.print_board()
        move(board, current_party)
        return
    # except Exception:
    #     print("Unknown error. Try again")
    #     move(board, current_party)
    #     return
    board.relocate(place, to)


def start_game(board, current_party=Party.White):
    print("Game has started")
    while(True):
        board.print_board()
        if(chessanalytics.is_check(board, current_party)):
            print("Check.")
            if(chessanalytics.is_mate(board, current_party)):
                print("Mate.")
                print(
                    "Player on {} wins the game".format(
                        next_move(current_party)))
                return
        if(chessanalytics.is_stalemate(board, current_party)):
            print("Stalemate.")
            print("Player on {} just stalemated the game".format(current_party))
            return
        print("Moves {}".format(current_party))
        try:
            move(board, current_party)
        except exceptions.Surrender:
            print("Team {} resigned".format(current_party))
            break
        current_party = next_move(current_party)
