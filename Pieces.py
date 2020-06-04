import sys


def create_piece_instance(piece, color="black", board=None):
    """Receives a piece name and returns an instance of it"""
    if piece is (None or ' '):
        return
    if len(piece) == 1:
        if piece.isupper():
            color = "white"
        else:
            color = "black"
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
        self.color = color
        self.board = board

    def place(self, board):
        """places piece on the board"""
        self.board = board

    def castle(self, pos):
        moves = []
        if not self.didnt_move:
            return []
        if self.color == "white":
            if pos[1] == "1" and ("A1" or "H1" in self.board):
                x = "B"
                y = pos[1]
                while x != pos[0]:
                    if x + y in self.board:
                        break
                    x = chr(ord(x) + 1)
                if x == "E":
                    moves.append(self.board.num_notation("C1"))
                x = "F"
                while x != "H":
                    if x + y in self.board:
                        break
                    x = chr(ord(x) + 1)
                if x == "H":
                    moves.append(self.board.num_notation("G1"))
        else:
            if pos[1] == "8" and ("A8" or "H8" in self.board):
                x = "B"
                y = pos[1]
                while x != pos[0]:
                    if x + y in self.board:
                        break
                    x = chr(ord(x) + 1)
                if x == "E":
                    moves.append(self.board.num_notation("C8"))
                x = "F"
                while x != "H":
                    if x + y in self.board:
                        break
                    x = chr(ord(x) + 1)
                if x == "H":
                    moves.append(self.board.num_notation("G8"))
        return moves

    def piece_moves(self, pos, line_movemant, diagonal_movemant, distance):
        """receives a set of variables and return the possible moves of each piece"""
        enemy = ("white" if self.color == "black" else "black")
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
            for single_move in range(1, distance + 1):
                """iterating over all possible moves in a specific line/diagonal """
                destination = starting_pos[0] + single_move * x, starting_pos[1] + single_move * y
                if board.alpha_notation(destination) not in board.occupied(self.color) and board.in_board(destination):
                    moves.append(destination)
                    if board.alpha_notation(destination) in board.occupied(enemy):
                        break
                else:
                    break
        if self.name == "K":
            moves = moves + self.castle(pos)
        return list(map(board.alpha_notation, moves))
        # instead of iterating over moves and using alpha_notation on its values we can use map


class King(Piece):
    name = "K"
    didnt_move = True

    def available_moves(self, pos):
        return super(King, self).piece_moves(pos.upper(), True, True, 1)


class Queen(Piece):
    name = "Q"

    def available_moves(self, pos):
        return super(Queen, self).piece_moves(pos.upper(), True, True, 8)


class Rook(Piece):
    name = "R"
    didnt_move = True

    def available_moves(self, pos):
        return super(Rook, self).piece_moves(pos.upper(), True, False, 8)


class Bishop(Piece):
    name = "B"

    def available_moves(self, pos):
        return super(Bishop, self).piece_moves(pos.upper(), False, True, 8)


class Knight(Piece):
    name = "N"

    def available_moves(self, pos):
        board = self.board
        moves = []
        unchecked_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
        starting_pos = board.num_notation(pos.upper())
        for (x, y) in unchecked_moves:
            destination = starting_pos[0] + x, starting_pos[1] + y
            if board.in_board((destination[0], destination[1])) and self.board.alpha_notation(destination) not in board.occupied(self.color):
                moves.append(destination)
        return list(map(board.alpha_notation, moves))  # instead of iterating over moves and alpha_notation it we can use map


class Pawn(Piece):
    name = "P"
    # change after moving

    def available_moves(self, pos):
        enemy = ("white" if self.color == "black" else "black")
        didnt_move = False
        board = self.board
        moves = []
        if self.color == "white":
            regular_move = (1, 0)
            first_move = (2, 0)
            capture = ((1, 1), (1, -1))
            if pos[1] == "2":
                didnt_move = True
        else:
            regular_move = (-1, 0)
            first_move = (-2, 0)
            capture = ((-1, -1), (-1, 1))
            if pos[1] == "7":
                didnt_move = True

        starting_pos = board.num_notation(pos.upper())
        destination = board.alpha_notation((starting_pos[0] + regular_move[0], starting_pos[1] + regular_move[1]))
        # regular and first moves column value is always 0
        if destination not in board.occupied("white") and destination not in board.occupied("black"):
            # if destination not occupied, if first square is taken we can't move to the next one
            moves.append(board.num_notation(destination))
            destination = board.alpha_notation((starting_pos[0] + first_move[0], starting_pos[1] + first_move[1]))
            # pawn's first move
            if destination not in board.occupied("white") and destination not in board.occupied("black") and didnt_move:
                moves.append(board.num_notation(destination))

        capture_dest = board.alpha_notation((starting_pos[0] + capture[0][0], starting_pos[1] + capture[0][1]))
        if capture_dest in board.occupied(enemy):
            moves.append(board.num_notation(capture_dest))
        capture_dest = board.alpha_notation((starting_pos[0] + capture[1][0], starting_pos[1] + capture[1][1]))
        # 2 captures options
        if capture_dest in board.occupied(enemy):
            moves.append(board.num_notation(capture_dest))
        return list(map(board.alpha_notation, moves))  # instead of iterating over moves we can use map





