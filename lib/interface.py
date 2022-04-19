from lib import chessmen
from PyQt5 import QtCore, QtGui, QtWidgets
import string

class Pawn(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.image = QtGui.QPixmap('pawn_light.svg')
        self.setMinimumSize(32, 32)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0, 0, self.image.scaled(
            size, size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


class Board(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.background = QtGui.QPixmap('chessboard480.svg')

        for i in range(8):
            layout.setRowStretch(i, 1)
            layout.setColumnStretch(i, 1)

        for col in range(8):
            layout.addWidget(Pawn(), 1, col)

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
        qp.drawPixmap(rect, self.background.scaled(rect.size(), 
            QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

class ChessGame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)
        self.board = Board()
        layout.addWidget(self.board)
        self.table = QtWidgets.QTableWidget(1, 3)
        layout.addWidget(self.table)

def get_move(current_party):
    place, to = input().translate({ord(c): 
        None for c in string.whitespace}).split("->")
    place = place.lower()
    to = to.lower()
    place = (ord(place[0]) - 97, ord(place[1]) - 49)
    place = (7 - place[1], place[0])
    to = (ord(to[0]) - 97, ord(to[1]) - 49)
    to = (7 - to[1], to[0])

    return (place, to)