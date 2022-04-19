from lib import chessmen, chess, exceptions
from PyQt5 import QtCore, QtGui, QtWidgets
import string
import copy
import sys

piece_map = {('p', chessmen.Party.White): 'data/pawn_light.svg',
             ('n', chessmen.Party.White): 'data/knight_light.svg',
             ('b', chessmen.Party.White): 'data/bishop_light.svg',
             ('q', chessmen.Party.White): 'data/queen_light.svg',
             ('k', chessmen.Party.White): 'data/king_light.svg',
             ('r', chessmen.Party.White): 'data/rook_light.svg',
             ('p', chessmen.Party.Black): 'data/pawn_dark.svg',
             ('n', chessmen.Party.Black): 'data/knight_dark.svg',
             ('b', chessmen.Party.Black): 'data/bishop_dark.svg',
             ('q', chessmen.Party.Black): 'data/queen_dark.svg',
             ('k', chessmen.Party.Black): 'data/king_dark.svg',
             ('r', chessmen.Party.Black): 'data/rook_dark.svg'}


class Piece(QtWidgets.QWidget):
    def __init__(self, piece):
        super().__init__()
        self.image = QtGui.QPixmap(piece_map[(piece.name, piece.party)])
        self.setMinimumSize(32, 32)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(
            0,
            0,
            self.image.scaled(
                size,
                size,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation))


class Board(QtWidgets.QWidget):
    def __init__(self, board):
        super().__init__()
        self.board = board
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.background = QtGui.QPixmap('data/chessboard480.svg')

        for i in range(8):
            layout.setRowStretch(i, 1)
            layout.setColumnStretch(i, 1)

        for row in range(8):
            for col in range(8):
                if(board.get_chessman((row, col)) is not None):
                    layout.addWidget(
                        Piece(
                            board.get_chessman(
                                (row, col))), row, col)

    def relocate(self, place, to):
        temp = copy.copy(Piece(board.get_chessman((place[0], place[1]))))
        layout.removeWidget(layout.itemAtPosition(place[0], place[1]).widget())
        layout.removeWidget(layout.itemAtPosition(to[0], to[1]).widget())
        layout.addWidget(temp, to[0], to[1])

    def minimumSizeHint(self):
        return QtCore.QSize(256, 256)

    def sizesHint(self):
        return QtCore.QSize(768, 768)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        rect = QtCore.QRect(0, 0, size, size)
        rect.moveCenter(self.rect().center())
        self.layout().setGeometry(rect)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        rect = self.layout().geometry()
        qp.drawPixmap(
            rect,
            self.background.scaled(
                rect.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation))


class ChessGame(QtWidgets.QMainWindow):
    def __init__(self, board):
        super().__init__()
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)
        self.board = Board(board)
        layout.addWidget(self.board)
        self.table = QtWidgets.QTableWidget(1, 3)
        layout.addWidget(self.table)
        QtCore.QThread.emit(SIGNAL("idle"))

    def relocate(self, place, to):
        self.board.relocate(place, to)
        QtCore.QThread.emit(SIGNAL("idle"))


def help():
    print("You can make a step like \"A1->B2\"")
    print("You can resign like \"surrender\"")
    print("You can see the current board \"board\"")
    print("You can save the game \"save")


def get_move(current_party):
    line = input()
    if(line == "help"):
        help()
        get_move(current_party)
    elif(line == "surrender"):
        raise exceptions.Surrender
    elif(line == "board"):
        raise exceptions.Board
    elif(line == "save"):
        raise exceptions.Save
    else:
        try:
            place, to = line.translate(
                {ord(c): None for c in string.whitespace}).split("->")
            place = place.lower()
            to = to.lower()
            place = (ord(place[0]) - 97, ord(place[1]) - 49)
            place = (place[1], place[0])
            to = (ord(to[0]) - 97, ord(to[1]) - 49)
            to = (to[1], to[0])
            return (place, to)
        except BaseException:
            raise exceptions.IncorrectMove
