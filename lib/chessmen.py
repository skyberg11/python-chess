from enum import Enum

class FigureType(Enum):
    VectorStroke = 1
    Finite = 2

class Party(Enum):
    White = 1
    Black = 2

def next_move(party):
    if(party == Party.White):
        return Party.Black
    else:
        return Party.White

class Chessmen:
    """Party, figure_type, name, cost
    Moves and vectors given in deltas relative to the
    current node"""
    def __init__(self, party, figure_type, name, cost):
        self.party = party
        self.figure_type = figure_type
        self.name = name
        self.cost = cost

    def set_vectors(self, *vectors):
        self.vectors = vectors

    def set_finite_moves(self, *moves):
        self.moves = moves

    def set_team(self, party):
        self.party = party