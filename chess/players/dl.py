import os

import chess
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class DeepLearning:
    def __init__(self):
        self.model = Model()
        self.model.load_state_dict(torch.load("models/model.pth"))

    def move(self, board):
        best_move = None
        best_white_score = -99999
        best_black_score = 99999
        for possible_move in board.legal_moves:
            new_board = board.copy()
            new_board.push(possible_move)
            encoded_board = torch.Tensor(self.bb2array(new_board)).unsqueeze(0)
            pred = self.model(encoded_board)
            if board.turn == chess.WHITE:
                if pred > best_white_score:
                    best_move = possible_move
                    best_white_score = pred
            elif board.turn == chess.BLACK:
                if pred < best_black_score:
                    best_move = possible_move
                    best_black_score = pred
        return best_move.uci()

    def bb2array(self, b):
        x = np.zeros((12, 8, 8), dtype=np.int8)
        piece_list = self.convert_to_int(b)
        for pos, piece in enumerate(piece_list):
            if piece != 0:
                col = int(pos % 8)
                row = int(pos / 8)
                x[piece - 1][row][col] = 1
        return x

    def convert_to_int(self, board):
        l = [None] * 64
        for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):
            l[sq] = board.piece_type_at(sq)
        for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):
            l[sq] = -board.piece_type_at(sq)
        return [0 if v is None else v for v in l]
