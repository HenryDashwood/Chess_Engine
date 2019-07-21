import chess
import random
import numpy as np

class Naive:
    def move(self, board):
        move = random.choice(list(board.legal_moves))
        return move.uci()
