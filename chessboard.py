from copy import deepcopy
import re

import Pieces

# First letters of the different pieces in the correct order.


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

    def all_available_moves(self, color):
        """ returns all the available moves for a player"""
        all_moves = []
        # iterating over dictionary's keys to return its available moves
        for coord in self.keys():
            if (self[coord] is not None) and self[coord].color == color:
                moves = self[coord].available_moves(coord)
                if moves:
                    all_moves += moves
        return all_moves
    '''
    def shift(self, pos1, pos2):
        pos1 = pos1.upper()
        pos2 = pos2.upper()
        piece = self[pos1]
        if pos2 in self:
            destination = pos2
        else:
            destination = None
        if self.player_turn != piece.color:
            print("Not %s's turn!" % piece.color)
        if piece.color == "black":
            enemy = "white"
        else:
            enemy = "black"
        available_moves = piece.available_moves(pos1)
        if pos2 not in available_moves:
            print("illegal move")
        """
        if self.all_available_moves(enemy):
            if self.all
        """
    '''
    def shift(self, p1, p2):
        p1, p2 = p1.upper(), p2.upper()
        piece = self[p1]
        if p2 in self:
            dest = self[p2]
        else:
            dest = None
        if self.player_turn != piece.color:
            print("It's not your turn!")
        moves_available = piece.available_moves(p1)
        if p2 not in moves_available:
            print("invalid move")
        else:
            self.move(p1, p2)
            #self.complete_move(piece, dest, p1, p2)

    def in_board(self, coord):
        return 0 <= coord[0] < 8 and 0 <= coord[1] < 8

    def move(self, pos1, pos2):
        piece = self[pos1]
        del self[pos1]
        # deletes pos1:piece from board's dictionary
        self[pos2] = piece
        enemy = ('white' if piece.color == 'black' else 'black')
        self.player_turn = enemy
        if self.king_captured(pos2, enemy):
            game_over()
            return
        if piece.name == 'P':
            if piece.color == 'white':
                if pos2[1] == '8':
                    del self[pos2]
                    self[pos2] = Pieces.create_piece_instance('Q', piece.color, self)
                    return
        if piece.name == 'r' or piece.name == 'k':
            if piece.didnt_move_yet:
                self.castle(piece)

    def alpha_notation(self, coords):
        """receives numbered coordinates and returns its place on the board (6,6) = ('G', 7)"""
        if not (0 <= coords[0] <= 7 and 0 <= coords[1] <= 7):
            return None
        return self.y_values[int(coords[1])] + str(int(coords[0]) + 1)

    def num_notation(self, coord):
        """receives lettered coordinates and returns its place on the matrix (G7 = (6, 6))"""
        return int(coord[1]) - 1, self.y_values.index(coord[0])

    def occupied(self, color):
        """returns all color player pieces' coordinates"""
        result = []
        for coord in self:
            # iterating over keys, every key is a coordinate
            if self[coord].color == color:
                result.append(coord)
        return result
    
    def king_captured(self, pos2, enemy):
        if pos2 in self.occupied(enemy):
            if self[pos2].name == 'K':
                return True
        return False

    def game_over(self):
        pass

    '''
    def complete_move(self, piece, dest, pos1, pos2):
        enemy = ('white' if piece.color == 'black' else 'black')

        if piece.color == 'black':
            self.fullmove_number += 1
        self.halfmove_clock += 1

        self.player_turn = enemy
        abbr = piece.name
        if abbr == 'P':
            abbr = ''
            self.halfmove_clock = 0
        if dest is None:
            movetext = abbr + pos2.lower()
        else:
            movetext = abbr + 'x' + pos2.lower()
            self.halfmove_clock = 0
        self.history.append(movetext)
    '''



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
                    continue

                coord = self.alpha_notation((7 - x, y))
                self[coord] = Pieces.create_piece_instance(char)
                self[coord].place(self)

        if pattern[1] == 'w':
            self.player_turn = 'white'
        else:
            self.player_turn = 'black'
            
        #self.halfmove_clock = int(pat[2])
        #self.fullmove_number = int(pat[3])

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










