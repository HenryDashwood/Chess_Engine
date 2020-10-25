import os

import chess
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from dl.models import Model1


class DeepLearning2:
    def __init__(self):
        self.model = Model1()
        self.model.load_state_dict(torch.load("models/model.pth"))

    def move(self, board):
        best_move = None
        best_white_score = -99999
        best_black_score = 99999
        for possible_move in board.legal_moves:
            new_board = board.copy()
            new_board.push(possible_move)
            encoded_board = torch.FloatTensor([self.get_bitboard(new_board)])
            print(encoded_board.shape)
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

    def get_bitboard(self, board):
        """
        params
        ------
        board : chess.pgn board object
            board to get state from
        returns
        -------
        bitboard representation of the state of the game
        64 * 6 + 5 dim binary numpy vector
        64 squares, 6 pieces, '1' indicates the piece is at a square
        5 extra dimensions for castling rights queenside/kingside and whose turn
        """
        bitboard = np.zeros(64 * 6 * 2 + 5)
        piece_idx = {"p": 0, "n": 1, "b": 2, "r": 3, "q": 4, "k": 5}
        for i in range(64):
            if board.piece_at(i):
                color = int(board.piece_at(i).color) + 1
                bitboard[
                    (piece_idx[board.piece_at(i).symbol().lower()] + i * 6) * color
                ] = 1
        bitboard[-1] = int(board.turn)
        bitboard[-2] = int(board.has_kingside_castling_rights(True))
        bitboard[-3] = int(board.has_kingside_castling_rights(False))
        bitboard[-4] = int(board.has_queenside_castling_rights(True))
        bitboard[-5] = int(board.has_queenside_castling_rights(False))
        return bitboard
