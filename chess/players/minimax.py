import random

import chess

from .player import Player

MAX_SCORE = 999999
MIN_SCORE = -999999


class Minimax(Player):
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def move(self, board):
        best_moves = []
        best_score = None
        best_black = MIN_SCORE
        best_white = MIN_SCORE
        for possible_move in board.legal_moves:
            next_state = board.copy()
            next_state.push(possible_move)
            opponent_best_outcome = self.best_result(
                next_state, self.max_depth, best_black, best_white
            )
            our_best_outcome = -1 * opponent_best_outcome
            if (not best_moves) or our_best_outcome > best_score:
                best_moves = [possible_move]
                best_score = our_best_outcome
                if board.turn == chess.BLACK:
                    best_black = best_score
                elif board.turn == chess.WHITE:
                    best_white = best_score
            elif our_best_outcome == best_score:
                best_moves.append(possible_move)
        return random.choice(best_moves).uci()

    def best_result(self, board, max_depth, best_black, best_white):
        if board.is_game_over(claim_draw=True):
            if (board.turn == chess.WHITE and board.result() == "1-0") or (
                board.turn == chess.BLACK and board.result() == "0-1"
            ):
                return MAX_SCORE
            else:
                return MIN_SCORE

        if max_depth == 0:
            return self.score(board)

        best_so_far = MIN_SCORE
        for candidate_move in board.legal_moves:
            next_state = board.copy()
            next_state.push(candidate_move)
            oppontent_best_result = self.best_result(
                next_state, max_depth - 1, best_black, best_white
            )
            our_result = -1 * oppontent_best_result
            if our_result > best_so_far:
                best_so_far = our_result

            if board.turn == chess.WHITE:
                if best_so_far > best_white:
                    best_white = best_so_far
                outcome_for_black = -1 * best_so_far
                if outcome_for_black < best_black:
                    return best_so_far
            elif board.turn == chess.BLACK:
                if best_so_far > best_black:
                    best_black = best_so_far
                outcome_for_white = -1 * best_so_far
                if outcome_for_white < best_white:
                    return best_so_far
        return best_so_far

    def score(self, board):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0,
        }
        score = 0.0
        piece_map = board.piece_map()
        for x in piece_map:
            piece_value = values[piece_map[x].piece_type]
            if piece_map[x].color == board.turn:
                score += piece_value
            else:
                score -= piece_value

        return score
