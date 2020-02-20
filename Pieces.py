import sys


def create_piece_instance(piece, color='black'):
    """Receives a piece name and returns an instance of it"""
    if piece is (None or ' '):
        return
    if len(piece) == 1:
        if piece.isupper():
            color = 'White'
        else:
            color = 'Black'
        piece = Piece.Short_Name[piece.upper()]
    module = sys.modules[__name__]
    return module.__dict__[piece](color)


class Piece(object):
    Short_Name = {
        "K": "King",
        "Q": "Queen",
        "R": "Rook",
        "B": "Bishop",
        "N": "Knight",
        "P": "Pawn"
    }

    def __init__(self, color):
        if color == 'Black':
            self.name = self.name.lower()
        elif color == 'White':
            self.name = self.name.upper()
        self.color = color

    def moves(self):
        pass

    def place(self, board):
        """ reference to the board """
        self.board = board


class King(Piece):
    name = 'k'
    moves = None


class Queen(Piece):
    name = 'q'
    moves = None


class Rook(Piece):
    name = 'r'
    moves = None


class Bishop(Piece):
    name = 'b'
    moves = None


class Knight(Piece):
    name = 'n'
    moves = None


class Pawn(Piece):
    name = 'p'
    moves = None




