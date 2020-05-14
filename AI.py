from chessboard import *

class AI:
    depth = 2
    counter = 0

    def __init__(self, board):
        self.board = board
        self.moves = self.board.all_boards("black")


    sign = {
        "white": -1,
        "black": 1
    }

    piece_value = {
        "K": 10000,
        "Q": 900,
        "R": 500,
        "B": 340,
        "N": 300,
        "P": 100
    }

    def scoring(self, board):
        score = 0
        black_n = 0
        white_n = 0
        for coord in board:
            name = board[coord].name
            color = board[coord].color
            if color == 'black':
                black_n = black_n + 1
            if color == 'white':
                white_n = white_n + 1
            score += self.sign[color] * self.piece_value[name]
        print("white =", white_n, " black = ", black_n)
        return score

    def minimax(self, board, depth, player_turn, alpha, beta):
        self.counter += 1
        if depth == 0:
            #if self.scoring(board) != 0:
            print("score = ", self.scoring(board), board.tolist("white"), "  ", board.missing_pieces("white"), " ", board.tolist("black"), "  ", board.missing_pieces("black"))
            return self.scoring(board)

        if player_turn == "black":
            max_score = float("-inf")
            boards = board.all_boards("black")
            for next_board in boards:
                score = self.minimax(next_board, depth - 1, "white", alpha, beta)
                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                #if beta < alpha:
                #    break
            return max_score

        else:
            min_score = float("inf")
            boards = board.all_boards("white")
            for next_board in boards:
                score = self.minimax(next_board, depth - 1, "black", alpha, beta)
                min_score = min(min_score, score)
                beta = min(beta, score)
                #if beta < alpha:
                #    break
            return min_score

    def ai_play(self):
        self.counter = 0
        moves = self.board.all_boards("black")
        best_score = float("-inf")
        best_move = moves[0]
        for move in moves:
            if 'H4' in move:
                print("here")
            score = self.minimax(move, self.depth, "black", float("inf"), float("-inf"))
            print("counter = ", self.counter)
            if score >= best_score:
                best_score = score
                best_move = move
            print("ai_ score ", score, move)
        """
        best_score = self.minimax(self.board, self.depth, "black")
        best_move = None
        scores = []
        moves = self.board.all_boards("black")[0]
        for move in moves:
            scores.append(self.scoring(move))
            if self.scoring(move) == best_score:
                best_move = move

        print("scores: ", scores)
        """
        pos1 = ""
        for coord in self.board:
            if coord not in best_move:
                pos1 = coord
                del self.board[coord]
                break
        for coord in best_move:
            if coord not in self.board or self.board[coord].color != best_move[coord].color:
                self.board[coord] = best_move[coord]
                self.board.player_turn = "white"
                return pos1 + "->" + coord


















