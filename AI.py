from chessboard import *


class AI:
    depth = 2

    def __init__(self, board):
        self.board = board
        self.moves = self.board.all_boards("black")

    sign = {
        "white": 1,
        "black": -1
    }

    piece_value = {
        'K': 10000,
        'Q': 900,
        'R': 500,
        'B': 340,
        'N': 300,
        'P': 100
    }

    def scoring(self, board):
        score = 0
        for coord in board:
            score += self.sign[str(board[coord].color)] * self.piece_value[str(board[coord].name)]
        return score

    """
    def min_board(self, curr_board, depth):
        if depth == 0:
            return curr_board
        boards = curr_board.all_boards("black")
        min_score = float("inf")
        for next_board in boards:
            score = self.scoring(curr_board, next_board)
            if score < min_score:
                min_score = score
        return min_score

    def max_board(self, curr_board, depth):
        if depth == 0:
            return curr_board
        boards = curr_board.all_boards("white")
        max_score = float("-inf")
        for next_board in boards:
            score = self.scoring(curr_board, next_board)
            if score > max_score:
                max_score = score
        return max_score
    """

    def minimax(self, board, depth):
        if depth == 0:
            return self.scoring(board), board

        if board.player_turn == "black":
            boards = board.all_boards("black")
            min_score = float("inf")
            for next_board in boards:
                score = self.minimax(next_board, depth - 1)[0]
                if score < min_score:
                    min_score = score
                    board = next_board
            return min_score, board

        else:
            boards = board.all_boards("white")
            max_score = float("-inf")
            for next_board in boards:
                score = self.minimax(next_board, depth - 1)[0]
                if score > max_score:
                    max_score = score
                    board = next_board
            return max_score, board

    def ai_play(self):
        move = self.minimax(self.board, self.depth)[1]
        pos1 = ""
        for coord in self.board:
            if coord not in move:
                pos1 = coord
                del self.board[coord]
                break
        for coord in move:
            if coord not in self.board:
                self.board[coord] = move[coord]
                self.board.player_turn = "white"
                return pos1 + "->" + coord


















