from copy import deepcopy
import re

import Pieces

# Start_pattern = {R : w, N : w, B : w, Q : w, K : w, B : w, N : w, R : w,}
START_PATTERN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 0 1'

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


    def move(self, p1, p2):
        piece = self[p1]
        if p2 in Pieces.possible_moves(p1):
            self.p2 = piece

    def show(self, pat):
        self.clear()
        pat = pat.split(' ')


