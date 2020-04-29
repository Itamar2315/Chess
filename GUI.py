from tkinter import *
from AI import *
import chessboard


class GUI:
    turn = "white"
    pieces = {}
    selected_piece = None
    focused = None
    pictures = {}
    board_color1 = "#E6CCAA"
    board_color2 = "#A85A0D"
    highlight_color = "#808080"
    rows = 8
    columns = 8
    square_size = 64

    def __init__(self, parent, board):
        self.chessboard = board
        self.parent = parent

        # Adding Frame
        self.btmfrm = Frame(parent, height=64)
        self.info_label = Label(self.btmfrm, text="   White's turn", fg="blue")
        self.info_label.pack(side=RIGHT, padx=8, pady=5)
        self.btmfrm.pack(fill="x", side=BOTTOM)

        canvas_height = self.rows * self.square_size
        canvas_width = self.columns * self.square_size
        self.canvas = Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.canvas.bind("<Button-1>", self.square_clicked)

    def new_game(self):
        self.chessboard.show(self.chessboard.START_PATTERN)
        self.draw_board()
        self.draw_pieces()
        self.info_label.config(text="   White's turn  ", fg="blue")

    def shift(self, pos1, pos2, dest_piece=None):
        # handles clicked piece situations
        piece = self.chessboard[pos1]
        if pos2 in self.chessboard:
            dest_piece = self.chessboard[pos2]

        if not dest_piece or dest_piece.color != piece.color:
            self.chessboard.shift(pos1, pos2)
            self.turn = ('white' if piece.color == 'black' else 'black')
            self.info_label[
                "text"] = '' + piece.color.capitalize() + ": " + pos1 + "->" + pos2 + ",    " + self.turn.capitalize() + \
                          "\'s turn"

    '''
    def shift(self, p1, p2):
        piece = self.chessboard[p1]
        try:
            dest_piece = self.chessboard[p2]
        except:
            dest_piece = None
        if dest_piece is None or dest_piece.color != piece.color:
            try:
                self.chessboard.shift(p1, p2)
            except chessboard.ChessError as error:
                self.info_label["text"] = error.__class__.__name__
            else:
                turn = ('white' if piece.color == 'black' else 'black')
                self.info_label[
                    "text"] = '' + piece.color.capitalize() + ": " + p1 + "->" + p2 + ',    ' + turn.capitalize() +\
                              '\'s turn'
        '''
    def square_clicked(self, event):
        col_size = row_size = self.square_size
        selected_column = int(event.x / col_size)
        # because the size of the board is column * square_size
        selected_row = 7 - int(event.y / row_size)
        # chess board's rows are arranged oppositely
        pos = self.chessboard.alpha_notation((selected_row, selected_column))

        """
        if self.chessboard.in_board((selected_row, selected_column)):
            if pos in self.chessboard:
                piece = self.chessboard[pos]
        """

        if self.selected_piece:
            self.shift(self.selected_piece[1], pos)
            self.selected_piece = None
            self.focused = None
            self.pieces = {}
            self.draw_board()
            self.draw_pieces()

        self.viable_piece_to_move(pos)
        self.draw_board()

        if self.turn == "black":
            ai = AI(self.chessboard)
            move = ai.ai_play()
            self.turn = "white"
            self.info_label[
                "text"] = '' + "Black: " + move + ",    " + self.turn.capitalize() + \
                          "\'s turn"
            self.selected_piece = None
            self.focused = None
            self.pieces = {}
            self.draw_board()
            self.draw_pieces()
            self.viable_piece_to_move(pos)
            self.draw_board()

    def viable_piece_to_move(self, pos, piece=None):
        if pos in self.chessboard:
            piece = self.chessboard[pos]
        if piece is not None and (piece.color == self.chessboard.player_turn):
            self.selected_piece = (self.chessboard[pos], pos)
            self.focused = list(map(self.chessboard.num_notation, (self.chessboard[pos].available_moves(pos))))
            
    def draw_board(self):
        current_color = self.board_color1
        for col in range(self.columns):
            current_color = self.board_color1 if current_color == self.board_color2 else self.board_color2
            for row in range(self.rows):
                # creating rectangle's vertexes
                p1_x = (col * self.square_size)
                p1_y = ((7 - row) * self.square_size)

                p2_x = p1_x + self.square_size
                p2_y = p1_y + self.square_size
                if self.focused and (row, col) in self.focused:
                    # highlights the piece's possible moves
                    self.canvas.create_rectangle(p1_x, p1_y, p2_x, p2_y, fill=self.highlight_color, tags="area")
                else:
                    self.canvas.create_rectangle(p1_x, p1_y, p2_x, p2_y, fill=current_color, tags="area")

                current_color = self.board_color1 if current_color == self.board_color2 else self.board_color2
        """
        for piece_name in self.pieces:
            #
            self.pieces[piece_name] = (self.pieces[piece_name][0], self.pieces[piece_name][1])
            x = (self.pieces[piece_name][1] * self.square_size) + int(self.square_size / 2)
            y = ((7 - self.pieces[piece_name][0]) * self.square_size) + int(self.square_size / 2)
            self.canvas.coords(piece_name, x, y)
        """
        self.canvas.tag_raise("occupied")
        self.canvas.tag_lower("area")

    def draw_pieces(self):
        self.canvas.delete("occupied")
        for coord, piece in self.chessboard.items():
            x, y = self.chessboard.num_notation(coord)
            if piece is not None:
                filename = "Pieces_pictures/%s%s.png" % (piece.color, piece.name)
                piecename = "%s%s%s" % (piece.name, x, y)
                if filename not in self.pictures:
                    self.pictures[filename] = PhotoImage(file=filename)
                self.canvas.create_image(0, 0, image=self.pictures[filename],
                                         tags=(piecename, "occupied"),
                                         anchor="c")
                x0 = (y * self.square_size) + int(self.square_size / 2)
                y0 = ((7 - x) * self.square_size) + int(self.square_size / 2)
                self.canvas.coords(piecename, x0, y0)


def main(board):
    root = Tk()
    root.title("Chess")
    gui = GUI(root, board)
    gui.draw_board()
    gui.draw_pieces()
    root.mainloop()


if __name__ == "__main__":
    game = chessboard.Board()
    main(game)
