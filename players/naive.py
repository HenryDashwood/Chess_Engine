import chess
import random
import numpy as np

class Naive:
    def move(self, board):
        move = random.choice(list(board.legal_moves))
        return move.uci()

class FastNaive:
    def __init__(self):
        self.dim = None
        self.point_cache = []

    def _update_cache(self, dim):
        self.dim = dim
        rows, cols = dim
        self.point_cache = []
        for r in range(1, rows+1):
            for c in range(1, cols+1):
                self.point_cache.append(Point(row=r, col=c))

    def move(self, game_state):
        dim = (game_state.board.num_rows, game_state.board.num_cols)
        if dim != self.dim:
            self._update_cache(dim)

        idx = np.arange(len(self.point_cache))
        np.random.shuffle(idx)
        for i in idx:
            p = self.point_cache[i]
            if game_state.is_valid_move(Move.play(p)):
                return Move.play(p)
        return Move.pass_turn()
