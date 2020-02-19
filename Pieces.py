


Short_Name = {
    "K": "King",
    "Q": "Quinn",
    "R": "Rook",
    "B": "Bishop",
    "KN": "Knight",
    "P": "Pawn"
}


class Piece(object):
    def __init__(self):
        if piece_isupper():
            color = 'white'
        else:
            color = 'black'
        piece = Short_Name[piece.upper()]

    def create_piece_instance(self, piece, color='black'):
        """Receives a piece name and returns an instance of it"""
        # if piece is None: return
        if piece.isupper():
            color = 'white'
        else:
            color = 'black'
        piece = Short_Name[piece.upper()]




