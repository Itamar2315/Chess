class AI:
    depth = 3
    #is_opening = False

    def __init__(self, board):
        self.board = board

    sign = {
        "white": -1,
        "black": 1
    }

    piece_value = {
        "K": 10000,
        "Q": 900,
        "R": 500,
        "B": 300,
        "N": 300,
        "P": 100
    }

    def scoring(self, board):
        score = 0
        for coord in board:
            name = board[coord].name
            color = board[coord].color
            score += self.sign[color] * self.piece_value[name]
            if name == "P":
                pos = board.num_notation(coord)
                score += 50 - (abs(pos[0] - 3.5) + abs(pos[1] - 3.5))

        return score

    def minimax(self, board, depth, color, alpha, beta):
        if depth == 0:
            return self.scoring(board)

        if color == "black":
            boards = board.all_boards("black")
            max_score = float("-inf")
            for board in boards:
                score = self.minimax(board, depth - 1, "white", alpha, beta)
                max_score = max(score, max_score)
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return max_score

        else:
            boards = board.all_boards("white")
            min_score = float("inf")
            for board in boards:
                score = self.minimax(board, depth - 1, "black", alpha, beta)
                min_score = min(score, min_score)
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return min_score

    def minimax_board(self, board, depth, color, alpha, beta):
        if depth == 0:
            return self.scoring(board), board

        if color == "black":
            boards = board.all_boards("black")
            best_board = boards[0]
            max_score = float("-inf")
            for board in boards:
                score = self.minimax_board(board, depth - 1, "white", alpha, beta)[0]
                if score > max_score:
                    max_score = score
                    best_board = board
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return max_score, best_board

        else:
            boards = board.all_boards("white")
            best_board = boards[0]
            min_score = float("inf")
            for board in boards:
                score = self.minimax_board(board, depth - 1, "black", alpha, beta)[0]
                if score < min_score:
                    min_score = score
                    best_board = board
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return min_score, best_board

    def ai_play(self):
        """
        opening = []
        for move in self.opening_moves:
            move, destination = move[:len(move) // 2], move[len(move) // 2:]
            if move in self.board:
                open_board = deepcopy(self.board)
                piece = open_board[move]
                del open_board[move]
                open_board[destination] = piece
                opening.append(open_board)
        """
        num_of_available_moves = 0
        for key in self.board:
            num_of_available_moves += len(self.board[key].available_moves(key))
        self.depth = 6 - (num_of_available_moves // 10)
        # maximum of depth 6, for every 10 moves of moves reduce depth
        if self.depth < 2:
            self.depth = 2
            # minimum of depth 2
        moves = self.board.all_boards("black")
        best_score = float("-inf")
        best_move = moves[0]
        for move in moves:
            score = self.minimax(move, self.depth, "white", float("-inf"), float("inf"))
            if score > best_score:
                best_score = score
                best_move = move
        """
        num_of_available_moves = 0
        for key in self.board:
            num_of_available_moves += len(self.board[key].available_moves(key))
        self.depth = 4 - (num_of_available_moves // 40)
        # number of available moves in the beginning of the game is 20 for white and 20 for black
        best_move = self.minimax(self.board, self.depth, "black", float("-inf"), float("inf"))[1]
        """
        pos = ""
        for coord in self.board:
            if coord not in best_move:
                pos = coord
                del self.board[coord]
                break
        for coord in best_move:
            if coord not in self.board or self.board[coord].color != best_move[coord].color:
                # if a coordinate isn't in self.board
                self.board[coord] = best_move[coord]
                self.board.player_turn = "white"
                return pos + "->" + coord


















