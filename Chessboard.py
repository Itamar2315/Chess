from copy import deepcopy
import re
from AI import *
import Pieces

# First letters of the different pieces in the correct order.


class Board(dict):
    y_values = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    player_turn = None
    START_PATTERN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 0 1'
    pattern_list = START_PATTERN.split(" ")
    promoted_now = False
    promote_pawn = False

    def __init__(self):
        """creates the starting board"""
        super().__init__()
        self.show(self.pattern_list)
        #ai = AI(self)
        #print(ai.scoring(self))

    def is_game_over(self):
        color = self.player_turn
        for key in self:
            if self[key].color == color:
                # checks if the player can play
                piece = self[key]
                if self.remove_king_checks(piece, piece.available_moves(key)):
                    # None = False, if this if statement is True there is a legal move
                    return False
        return True

    """
    def missing_pieces(self, color):
        if len(self) == 32:
            return []
        missing = []
        start = {"R": 2, "N": 2, "P": 8, "K": 1, "Q": 1, "B": 2}
        current = {"R": 0, "N": 0, "P": 0, "K": 0, "Q": 0, "B": 0}
        for coord in self:
            if self[coord].color == color:
                current[self[coord].name] += 1
        for key in start:
            for i in range(start[key] - current[key]):
                missing.append(key)
        return missing
    """

    def all_boards(self, color):
        """ returns all the available boards(after moving) for a board"""
        boards = []
        # iterating over dictionary's keys to return its available moves
        for coord in self.keys():
            if self[coord].color == color:
                # all_moves.append(self[coord].available_moves(coord))
                available_moves = self.remove_king_checks(self[coord], self[coord].available_moves(coord))
                for move in available_moves:
                    board = deepcopy(self)
                    board.move(coord, move, False)
                    boards.append(board)
                    """
                    if board.promoted_now:
                        pos = move
                        board[pos] = Pieces.create_piece_instance('N', color, self)
                        # move
                        boards.append(board)
                        self.promoted_now = False
                    """
        return boards

    def remove_king_checks(self, piece, moves):
        """removes illegal moves (if king is checked)"""
        rmv_moves = []
        king_pos = None
        pos = None
        enemy = ("white" if piece.color == "black" else "black")
        for key in self:
            if self[key].name == "K":
                king_pos = key
            if piece == self[key]:
                pos = key
        for move in moves:
            king_in_check = False
            move_board = deepcopy(self)
            del move_board[pos]
            move_board[move] = piece
            if piece.name == "K":
                king_pos = move
            for key in move_board:
                if move_board[key].color == enemy:
                    for enemy_move in move_board[key].available_moves(key):
                        if enemy_move == king_pos:
                            king_in_check = True
                            break
                if king_in_check:
                    rmv_moves.append(move)
                    break
        for move in rmv_moves:
            moves.remove(move)
        return moves

    def shift(self, p1, p2, not_ai_turn):
        # checks its the player's and if his move is valid
        p1, p2 = p1.upper(), p2.upper()
        piece = self[p1]

        if self.player_turn != piece.color:
            print("It's not your turn!")
            return False
        moves_available = self.remove_king_checks(piece, piece.available_moves(p1))
        if p2 not in moves_available:
            print("invalid move")
            return False
        else:
            self.move(p1, p2, not_ai_turn)
            return True

    def in_board(self, coord):
        return 0 <= coord[0] < 8 and 0 <= coord[1] < 8

    def move(self, pos1, pos2, not_ai_turn):
        piece = self[pos1]
        del self[pos1]
        # deletes pos1:piece from board's dictionary
        self[pos2] = piece
        enemy = ("white" if piece.color == "black" else "black")
        self.player_turn = enemy

        if piece.name == 'P':
            if piece.color == "white":
                if pos2[1] == '8':
                    if not_ai_turn:
                        # pawn promotion
                        """
                        del self[pos2]
                        print("Write your preferable piece, Q/KN")
                        prefer = ""
                        while prefer != 'Q' and prefer != 'KN':
                            prefer = input()
                            if prefer == 'Q':
                                self[pos2] = Pieces.create_piece_instance('Q', piece.color, self)
                            elif prefer == 'KN':
                                self[pos2] = Pieces.create_piece_instance('N', piece.color, self)
                            else:
                                print("Please type your preference again")
                        """
                        self.player_turn = piece.color
                        self.promote_pawn = True
                        return

                    else:
                        del self[pos2]
                        self[pos2] = Pieces.create_piece_instance('Q', piece.color, self)
                        self.promoted_now = True

            elif pos2[1] == '1':
                # pawn becomes queen
                del self[pos2]
                self[pos2] = Pieces.create_piece_instance('Q', piece.color, self)
                return

        if piece.name == 'K' and piece.didnt_move:
            piece.didnt_move = False
            diff = ord(pos2[0]) - ord(pos1[0])

            if piece.color == "white":
                if diff == 2:
                    # move rook (castle)
                    pos1 = "H1"
                    pos2 = chr(ord(pos2[0]) - 1) + '1'
                    piece = self[pos1]
                    del self[pos1]
                    self[pos2] = piece
                elif diff == -2:
                    # move rook (castle)
                    pos1 = "A1"
                    pos2 = chr(ord(pos2[0]) + 1) + '1'
                    piece = self[pos1]
                    del self[pos1]
                    self[pos2] = piece

            else:
                if diff == 2:
                    # move rook (castle)
                    pos1 = "H8"
                    pos2 = chr(ord(pos2[0]) - 1) + '8'
                    piece = self[pos1]
                    del self[pos1]
                    self[pos2] = piece
                elif diff == -2:
                    # move rook (castle)
                    pos1 = "A8"
                    pos2 = chr(ord(pos2[0]) + 1) + '8'
                    piece = self[pos1]
                    del self[pos1]
                    self[pos2] = piece

        if piece.name == 'R':
            piece.didnt_move = False

    def alpha_notation(self, coords):
        """receives numbered coordinates and returns its place on the board (6,6) = 'G7' """
        if not (0 <= coords[0] <= 7 and 0 <= coords[1] <= 7):
            return None
        return self.y_values[int(coords[1])] + str(int(coords[0]) + 1)

    def num_notation(self, coord):
        """receives lettered coordinates and returns its place on the matrix 'G7' = (6, 6)"""
        return int(coord[1]) - 1, self.y_values.index(coord[0])

    def occupied(self, color):
        """returns all color player pieces' coordinates"""
        result = []
        for coord in self:
            # iterating over keys, every key is a coordinate
            if self[coord].color == color:
                result.append(coord)
        return result

    def show(self, pattern):
        """Receives pattern and creates it on the board"""
        self.clear()

        def expand(match):
            # encapsulate expand, expand returns (num * ' ', 3 = '   ') based on the num in the re
            return ' ' * int(match.group(0))

        pattern[0] = re.compile(r'\d').sub(expand, pattern[0])
        # re = regular expression, pattern is a regular expression
        for x, row in enumerate(pattern[0].split('/')):
            for y, char in enumerate(row):
                if char == ' ':
                    continue

                coord = self.alpha_notation((7 - x, y))
                self[coord] = Pieces.create_piece_instance(char)
                self[coord].place(self)

        if pattern[1] == 'w':
            self.player_turn = "white"
        else:
            self.player_turn = "black"




