import chess
import random
import time

class Classic:

    def __init__(self):
        self.time_limit = 2
        self.start_time = None
        self.MAXVAL = 10000
        self.best_move = None

    def move(self, board):
        self.start_time = time.time()

        depth = 1
        while (True):
            move = self.alphabeta(board, depth)
            if move:
                self.best_move = move
            depth += 1

            if self.time_up():
                return self.best_move

    def alphabeta(self, board, depth, alpha=float("-inf"), beta=float("inf")):
        best_current_move = list(board.legal_moves)[0]
        for m in board.legal_moves:
            if self.time_up():
                return best_current_move.uci()
            new_board = board.copy()
            new_board.push(m)
            score = self.min_value(new_board, depth-1, alpha, beta)
            if score > alpha:
                alpha = score
                best_current_move = m
        return best_current_move.uci()

    def min_value(self, board, depth, alpha, beta):
        if depth == 0:
            return self.score(board)
        for m in board.legal_moves:
            if self.time_up():
                break
            new_board = board.copy()
            new_board.push(m)
            score = self.max_value(new_board, depth-1, alpha, beta)
            if score < beta:
                beta = score
                if beta <= alpha:
                    break
        return beta

    def max_value(self, board, depth, alpha, beta):
        if depth == 0:
            return self.score(board)
        for m in board.legal_moves:
            if self.time_up():
                break
            new_board = board.copy()
            new_board.push(m)
            score = self.min_value(new_board, depth-1, alpha, beta)
            if score > alpha:
                alpha = score
                if alpha >= beta:
                    break
        return alpha

    def score(self, board):
        if board.is_game_over():
            if board.result() == "1-0":
                return self.MAXVAL
            elif board.result() == "0-1":
                return -self.MAXVAL
            else:
                return 0

        values = {chess.PAWN:1,chess.KNIGHT:3,chess.BISHOP:3,chess.ROOK:5,chess.QUEEN:9,chess.KING:0}
        score = 0.0
        # score += 10 if board.is_capture(move)
        piece_map = board.piece_map()
        for x in piece_map:
            piece_value = values[piece_map[x].piece_type]
            if piece_map[x].color == board.turn:
                score += piece_value
            else:
                score -= piece_value

        # actual_turn = board.turn
        # board.turn = chess.WHITE
        # score += 0.1 * board.legal_moves.count()
        # board.turn = chess.BLACK
        # score -= 0.1 * board.legal_moves.count()
        # board.turn = actual_turn

        return score

    def time_up(self):
        return time.time() > self.start_time + self.time_limit

class Human:

    def move(self, board):
        uci = self.get_move("Your move: ")
        legal_uci_moves = [move.uci() for move in board.legal_moves]
        while uci not in legal_uci_moves:
            print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
            uci = self.get_move("%s's move[q to quit]> " % board.who(board.turn))
        return uci

    def get_move(self, prompt):
        move = input(prompt)
        if move and move[0] == "q":
            raise KeyboardInterrupt()
        try:
            chess.Move.from_uci(move)
        except:
            move = None
        return move

class Random:

    def move(self, board):
        move = random.choice(list(board.legal_moves))
        return move.uci()
