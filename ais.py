import chess
import random

class Random:

    def __init__(self, board):
        self.board = board

    def move(self):
        move = random.choice(list(self.board.legal_moves))
        return move.uci()
