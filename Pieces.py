import sys


def create_piece_instance(piece, color='black', board=None):
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
    return module.__dict__[piece](color, board)


class Piece(object):
    Short_Name = {
        "K": "King",
        "Q": "Queen",
        "R": "Rook",
        "B": "Bishop",
        "N": "Knight",
        "P": "Pawn"
    }

    def __init__(self, color, board=None):
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
        unchecked_moves = ()
        line = ((0, 1), (1, 0), (-1, 0), (0, -1))
        diag = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        starting_pos = board.num_notation(pos.upper())
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

    def available_moves(self, pos):
        return super(King, self).moves(pos.upper(), True, True, 1)


class Queen(Piece):
    name = 'q'

    def available_moves(self, pos):
        return super(Queen, self).moves(pos.upper(), True, True, 8)


class Rook(Piece):
    name = 'r'

    def available_moves(self, pos):
        return super(Rook, self).moves(pos.upper(), True, False, 8)


class Bishop(Piece):
    name = 'b'

    def available_moves(self, pos):
        return super(Bishop, self).moves(pos.upper(), False, True, 8)


class Knight(Piece):
    name = 'n'

    def available_moves(self, pos):
        moves = []
        unchecked_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
        starting_pos = board.num_notation(pos.upper())
        for (x, y) in unchecked_moves:
            destination = starting_pos[0] + (x, y)
            if self.board.alpha_notation(destination) not in self.board.occupied('white') or self.board.occupied('black'):
                moves.append(destination)
            elif self.board.alpha_notation(destination) not in self.board.occupied(self.color):
                # capture
                moves.append(destination)
                blocked = True
        return map(board.num_notation, moves)  # instead of iterating over moves we can use map


class Pawn(Piece):
    name = 'p'

    def available_moves(self, pos):
        moves = []
        unchecked_moves = (())
        starting_pos = board.num_notation(pos.upper())
        for (x, y) in unchecked_moves:
            destination = starting_pos[0] + (x, y)
            if self.board.alpha_notation(destination) not in self.board.occupied('white') or self.board.occupied(
                    'black'):
                moves.append(destination)
            elif self.board.alpha_notation(destination) not in self.board.occupied(self.color):
                # capture
                moves.append(destination)
                blocked = True
        return map(board.num_notation, moves)  # instead of iterating over moves we can use map





