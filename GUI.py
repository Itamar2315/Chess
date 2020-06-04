from tkinter import *
import Chessboard
import Pieces
from copy import deepcopy
from AI import *


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

        # adding frame
        self.mvframe = Frame(parent, height=64)
        self.info_label = Label(self.mvframe, text="   White's turn", fg="blue")
        self.info_label.pack(side=RIGHT, padx=8, pady=5)
        self.mvframe.pack(fill="x", side=BOTTOM)

        # adding "new game" button
        self.ngframe = Frame(parent, height=64)
        self.ngbutton = Button(self.ngframe, text="New game", command=self.new_game)
        self.ngbutton.pack(side=LEFT, padx=12)
        self.ngframe.pack(fill="x", side=TOP)

        self.rebutton = Button(self.ngframe, text="Resign")
        self.rebutton.pack(side=LEFT, padx=30)
        self.rebutton.bind("<Button-1>", self.game_over)
        self.ngframe.pack(fill="x", side=TOP)

        canvas_height = self.rows * self.square_size
        canvas_width = self.columns * self.square_size
        self.canvas = Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.canvas.bind("<Button-1>", self.square_clicked)
        self.promotion_label = None
        self.promotion_frame = None

    def new_game(self, event=None):
        self.canvas.destroy()
        self.info_label.destroy()
        self.ngframe.destroy()
        self.mvframe.destroy()
        start_game()

    def shift(self, pos1, pos2, dest_piece=None):
        # shift from selected piece to Chessboard class
        piece = self.chessboard[pos1]
        if pos2 in self.chessboard:
            dest_piece = self.chessboard[pos2]

        if not dest_piece or dest_piece.color != piece.color:
            played = self.chessboard.shift(pos1, pos2, True)
            if played:
                if self.chessboard.promote_pawn:
                    self.selected_piece = None
                    self.focused = None
                    self.draw_board()
                    self.draw_pieces()
                    self.pawn_promotion()
                self.turn = ('white' if piece.color == 'black' else 'black')
                self.info_label[
                    "text"] = '' + piece.color.capitalize() + ": " + pos1 + "->" + pos2 + ",    " + self.turn.capitalize() + \
                              "\'s turn"

    def square_clicked(self, event=None):
        if self.chessboard.player_turn == "white":
            col_size = row_size = self.square_size
            selected_column = int(event.x / col_size)
            # because the size of the board is column * square_size
            selected_row = 7 - int(event.y / row_size)
            # chess board's rows are arranged oppositely
            pos = self.chessboard.alpha_notation((selected_row, selected_column))

            if self.selected_piece:
                self.shift(self.selected_piece[1], pos)
                self.selected_piece = None
                self.focused = None
                self.draw_board()
                self.draw_pieces()

            self.viable_piece_to_move(pos)
            self.draw_board()
            self.canvas.update()
            for coord in self.chessboard:
                # updating piece's board
                self.chessboard[coord].place(self.chessboard)

        if not self.chessboard.promote_pawn:
            if self.chessboard.is_game_over():
                self.game_over()

        if self.chessboard.player_turn == "black":
            og = deepcopy(self.chessboard)
            boards = self.chessboard.all_boards("white")
            for board in boards:
                self.chessboard = board
                self.draw_board()
                self.draw_pieces()
            self.chessboard = og
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
            if self.chessboard.is_game_over():
                self.game_over()

    def pawn_promotion(self):
        print("promo")
        self.canvas.unbind("<Button-1>")
        self.promotion_frame = Frame(root)
        self.promotion_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.promotion_frame.config(height=100, width=100)
        self.promotion_label = Label(self.promotion_frame, text="Your pawn is being promted.\nPick your desired piece.", font=("ariel", 12))
        self.promotion_label.grid(row=0, column=0, sticky=(W, E, N, S), columnspan=2)

        queen_button = Button(self.promotion_frame, text="Queen")
        queen_button.grid(row=1, column=0)
        queen_button.bind("<Button-1>", self.pawn_promotion_quinn)

        knight_button = Button(self.promotion_frame, text="Knight")
        knight_button.grid(row=1, column=1)
        knight_button.bind("<Button-1>", self.pawn_promotion_knight)

    def pawn_promotion_quinn(self, event=None):
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.square_clicked)
        self.promotion_frame.destroy()
        board = self.chessboard
        for key in board:
            # only white player can choose
            if key[1] == '8' and board[key].name == "P":
                board[key] = Pieces.create_piece_instance('Q', "white", board)

        for coord in self.chessboard:
            # updating piece's board
            self.chessboard[coord].place(self.chessboard)

        self.draw_board()
        self.draw_pieces()
        self.canvas.update()

        self.chessboard.player_turn = "black"
        self.square_clicked()

    def pawn_promotion_knight(self, event=None):
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.square_clicked)
        self.promotion_frame.destroy()
        board = self.chessboard
        for key in board:
            if key[1] == '8' and board[key].name == "P":
                board[key] = Pieces.create_piece_instance('N', "white", board)

        self.draw_pieces()
        for coord in self.chessboard:
            # updating piece's board
            self.chessboard[coord].place(self.chessboard)

        self.draw_board()
        self.draw_pieces()
        self.canvas.update()

        self.chessboard.player_turn = "black"
        self.square_clicked()

    def viable_piece_to_move(self, pos, piece=None):
        # checks if the player can move this piece
        if not self.chessboard.promote_pawn:
            if pos in self.chessboard:
                piece = self.chessboard[pos]
            if piece is not None and (piece.color == self.chessboard.player_turn):
                self.selected_piece = (piece, pos)
                self.focused = list(map(self.chessboard.num_notation, self.chessboard.remove_king_checks(piece, (piece.available_moves(pos)))))
            
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

        self.canvas.tag_raise("occupied")
        self.canvas.tag_lower("area")

    def draw_pieces(self):
        self.canvas.delete("occupied")
        for coord, piece in self.chessboard.items():
            x, y = self.chessboard.num_notation(coord)
            if piece is not None:
                short_name = piece.name.capitalize()
                filename = "Pieces_pictures/%s%s.png" % (piece.color[0].upper(), piece.Short_Name[short_name])
                piecename = "%s%s%s" % (piece.name, x, y)
                if filename not in self.pictures:
                    self.pictures[filename] = PhotoImage(file=filename)
                self.canvas.create_image(0, 0, image=self.pictures[filename],
                                         tags=(piecename, "occupied"),
                                         anchor="c")
                x0 = (y * self.square_size) + int(self.square_size / 2)
                y0 = ((7 - x) * self.square_size) + int(self.square_size / 2)
                self.canvas.coords(piecename, x0, y0)

    def game_over(self, event=None):
        if event:
            # if there's an event it means the player has resigned
            victory_label = Label(root, text="black is victorious!", font=("ariel", 26))
            victory_label.place(relx=0.5, rely=0.5, anchor="center")
            self.canvas.unbind("<Button-1>")
            return
        board = self.chessboard
        white_no_moves = True
        color = "white"
        is_tie = True

        for key in board:
            if board[key].color == "white":
                piece = board[key]
                legal_moves = board.remove_king_checks(piece, piece.available_moves(key))
                if legal_moves:
                    white_no_moves = False
                    # if white has legal moves
                    for move in legal_moves:
                        if move in board:
                            if board[move].name == "K":
                                is_tie = False
                    color = "white"
                    break

        if white_no_moves:
            color = "black"

        for key in board:
            if board[key].color == "black":
                piece = board[key]
                legal_moves = board.remove_king_checks(piece, piece.available_moves(key))
                if legal_moves:
                    # if black has legal moves
                    for move in legal_moves:
                        if move in board:
                            if board[move].name == "K":
                                is_tie = False
                    color = "black"
                    # black and white can move => white has resigned
                    break

        # checks if it's a draw or a checkmate
        board = deepcopy(board)
        board.player_turn = color
        for key in board:
            if board[key].color == color:
                piece = board[key]
                legal_moves = piece.available_moves(key)
                for move in legal_moves:
                    if move in board:
                        if board[move].name == "K":
                            is_tie = False

        if is_tie:
            tie_label = Label(root, text="Draw!", font=("ariel", 26))
            tie_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            victory_label = Label(root, text=color + " is victorious!", font=("ariel", 26))
            victory_label.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas.unbind("<Button-1>")


def print_rules():
    rules = open("Rules.txt", "r", encoding="utf-8")
    rules = rules.read()
    root.rules_label = Label(root, text=rules)
    root.rules_label.pack()
    root.bind('<Return>', start_game)


def start_game(event=None):
    root.rules_label.destroy()
    board = Chessboard.Board()
    root.title("Chess")
    gui = GUI(root, board)
    gui.draw_board()
    gui.draw_pieces()


def main():
    root.title("Chess")
    print_rules()
    root.mainloop()


root = Tk()
if __name__ == "__main__":
    main()
