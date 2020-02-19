from copy import deepcopy
import re

import Pieces

# Start_pattern = {R : w, N : w, B : w, Q : w, K : w, B : w, N : w, R : w,}
START_PATTERN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 0 1'
PATTERN_LIST = START_PATTERN.split(" ")
# First letters of the different pieces in the correct order.


def expand(match):
    # encapsulate expand
    return ' ' * int(match.group(0))


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

    def __init__(self):
        self.show(PATTERN_LIST)

    def move(self, p1, p2):
        piece = self[p1]
        if p2 in Pieces.possible_moves(p1):
            self.p2 = piece

    def show(self, pattern):
        """Receives pattern and creates it on the board"""
        self.clear()
        # turns p
        pattern[0] = re.compile(r'\d').sub(expand, pattern[0])
        # re = regular expression, pattern is a regular expression
        # turns decimal nums in the expression to (white spaces)*num.  2 = "  "
        print(pattern[0])





