from copy import deepcopy
import re

import Pieces

# First letters of the different pieces in the correct order.


def in_board(row, column):
    return 0 <= row <= 8 and 0 <= column <= 8


class Board(dict):
    y_values = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    x_values = (1, 2, 3, 4, 5, 6, 7, 8)
    captured_pieces = {'white': [], 'black': []}
    player_turn = None
    halfmove_clock = 0
    fullmove_number = 1
    history = []
    START_PATTERN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 0 1'
    pattern_list = START_PATTERN.split(" ")

    def __init__(self):
        """creates the starting board"""
        super().__init__()
        self.show(self.pattern_list)

    def move(self, p1, p2):
        piece = self[p1]
        if p2 in Pieces.possible_moves(p1):
            self[p2] = piece

    def alpha_notation(self, coords):
        """receives numbered coordinates and returns its place on the board (6,6) = ('G', 7)"""
        if not (0 <= coords[0] <= 7 and 0 <= coords[1] <= 7):
            return None
        return self.y_values[int(coords[1])] + str(int(coords[0]) + 1)

    def num_notation(self, coords):
        """receives lettered coordinates and returns its place on the matrix (G7 = (6, 6))"""
        return int(coords[1]) - 1, self.y_values.index(coords[0])

    def show(self, pattern):
        """Receives pattern and creates it on the board"""
        self.clear()

        def expand(match):
            # encapsulate expand, expand returns num * ' '  based on the num in the re
            return ' ' * int(match.group(0))
        pattern[0] = re.compile(r'\d').sub(expand, pattern[0])
        # re = regular expression, pattern is a regular expression
        for x, row in enumerate(pattern[0].split('/')):
            for y, char in enumerate(row):
                if char == ' ':
                    # skip
                    continue
                coord = self.alpha_notation((7 - x, y))
                self[coord] = Pieces.create_piece_instance(char)
                self[coord].board = self

        """
        def show(self, pat):
        self.clear()
        pat = pat.split(' ')

        def expand(match):
            return ' ' * int(match.group(0))

        pat[0] = re.compile(r'\d').sub(expand, pat[0])
        for x, row in enumerate(pat[0].split('/')):
            for y, letter in enumerate(row):
                if letter == ' ': continue
                coord = self.alpha_notation((7 - x, y))
                self[coord] = pieces.create_piece(letter)
                self[coord].place(self)
        if pat[1] == 'w':
            self.player_turn = 'white'
        else:
            self.player_turn = 'black'
        self.halfmove_clock = int(pat[2])
        self.fullmove_number = int(pat[3])
        
        
        def alpha_notation(self, xycoord):
        if xycoord[0] < 0 or xycoord[0] > 7 or xycoord[1] < 0 or xycoord[
            1] > 7: return
        return self.y_axis[int(xycoord[1])] + str(self.x_axis[int(xycoord[0])])
        
        """






