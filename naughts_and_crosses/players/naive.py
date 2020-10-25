import random


class Naive:
    def move(self, board):
        row, col = random.choice(board.legal_moves())
        return row, col
