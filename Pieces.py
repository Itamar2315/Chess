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
        self.board = board

    def moves(self, pos, line_movemant, diagonal_movemant, distance):
        """receives a set of variables and return the possible moves of each piece"""
        board = self.board
        moves = []
        line = ((0, 1), (1, 0), (-1, 0), (0, -1))
        diagonal = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        starting_pos = board.num_notation
        if line_movemant and diagonal_movemant:
            unchecked_moves = line + diag
        elif diagonal_movemant:
            unchecked_moves = diag
        elif line_movemant:
            unchecked_moves = line
        for (x, y) in unchecked_moves:
            blocked = false
            for single_move in range(1, distance + 1):
                """iterating over all possible moves in a specific line/diagonal """
                destination = starting_pos[0] + single_move * x, starting_pos[1] + single_move * y
                if self.board.alpha_notation(destination) not in board.occupied('white') or board.occupied('black'):
                    moves.append(destination)
                elif self.board.alpha_notation(destination) not in board.occupied(self.color):
                    # capture
                    moves.append(destination)
                    blocked = True
                else:
                    blocked = True
                if blocked:
                    break


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




