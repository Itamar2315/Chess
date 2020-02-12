from tkinter import *
from PIL import Image, ImageTk
import chessboard


class BoardGUI:
    pieces = {}
    focused = None
    pictures = {}
    board_color1 = "#DDC3AA"
    board_color2 = "#AB5500"
    highlight_color = "#808080"
    rows = 8
    columns = 8
    square_size = 64

    def __init__(self, parent, chessboard):
        self.chessboard = chessboard
        self.parent = parent



        # Adding Frame
        self.btmfrm = Frame(parent, height=64)
        self.info_label = Label(self.btmfrm, text="   White to Start the Game  ", fg='blue')
        self.info_label.pack(side=RIGHT, padx=8, pady=5)
        self.btmfrm.pack(fill="x", side=BOTTOM)

        canvas_height = self.rows * self.square_size
        canvas_width = self.columns * self.square_size
        self.canvas = Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.canvas.bind("<Button-1>", self.square_clicked)

    def new_game(self):
        self.chessboard.show(chessboard.START_PATTERN)
        self.draw_board()
        # self.draw_pieces()
        # self.info_label.config(text="   White's turn  ", fg='blue')

    def square_clicked(self, event):
        col_size = row_size = self.square_size
        selected_column = int(event.x / col_size)
        # because the size of the board is column * square_size
        selected_row = 7 - int(event.y / row_size)
        # chess board's rows are arranged oppositely
        if chessboard.in_board(selected_column, selected_row):
            return selected_column, selected_row
        return -1, -1

    def selected_piece(self, column, row):
        ''' this program is called only if the coordinates are inside the board '''
        pass

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

                if self.focused is not None and (row, col) in self.focused:
                    pass

                else:
                    self.canvas.create_rectangle(p1_x, p1_y, p2_x, p2_y, fill=current_color)
                current_color = self.board_color1 if current_color == self.board_color2 else self.board_color2

    def draw_pieces(self):
        self.canvas.delete("occupied")
        for coordinate, piece in self.chessboard.items():
            x, y = self.chessboard.num_notation(coordinate)
            if piece is not None:
                filename = "pieces_image/%s%s.png" % (piece.color, piece_name)
                piecename = "%s%s%s" % (piece_name, x, y)
                if filename not in self.images:
                    self.images[filename] = tk.PhotoImage(file=filename)
                self.canvas.create_image(0, 0, image=self.images[filename],
                                         tags=(piecename, "occupied"),
                                         anchor="c")
                x0 = (y * self.dim_square) + int(self.dim_square / 2)
                y0 = ((7 - x) * self.dim_square) + int(self.dim_square / 2)
                self.canvas.coordinates(piecename, x0, y0)


def main(chessboard):
    root = Tk()
    root.title("Chess")
    gui = BoardGUI(root, root)
    gui.draw_board()
    gui.draw_pieces()
    root.mainloop()


if __name__ == "__main__":
    game = chessboard.Board()
    main(game)
