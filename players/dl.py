import chess
import numpy as np
import os
import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepLearning:
    def __init__(self):
        self.model = Model()
        self.model.load_state_dict(torch.load('models/model.pth'))
        

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
    
    
    def convert_to_int(self, board):
        l = [None] * 64
        # Check if white
        for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):
            l[sq] = board.piece_type_at(sq)
        # Check if black
        for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):
            l[sq] = -board.piece_type_at(sq)
        return [0 if v is None else v for v in l]


    def bb2array(self, b):
        x = np.zeros((12,8,8), dtype=np.int8)
        piece_list = self.convert_to_int(b)

        for pos, piece in enumerate(piece_list):
            if piece != 0:
                col = int(pos % 8)
                row = int(pos / 8)
                x[piece-1][row][col] = 1

        return x
    
    
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.a1 = nn.Conv2d(12, 16, kernel_size=3, padding=1)
        self.a2 = nn.Conv2d(16, 16, kernel_size=3, padding=1)
        self.a3 = nn.Conv2d(16, 32, kernel_size=3, stride=2)

        self.b1 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.b2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.b3 = nn.Conv2d(32, 64, kernel_size=3, stride=2)

        self.c1 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.c2 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.c3 = nn.Conv2d(64, 128, kernel_size=2, stride=2)

        self.d1 = nn.Conv2d(128, 128, kernel_size=1)
        self.d2 = nn.Conv2d(128, 128, kernel_size=1)
        self.d3 = nn.Conv2d(128, 128, kernel_size=1)

        self.last = nn.Linear(128, 1)
        
    def forward(self, x):
        x = F.relu(self.a1(x))
        x = F.relu(self.a2(x))
        x = F.relu(self.a3(x))

        # 4x4
        x = F.relu(self.b1(x))
        x = F.relu(self.b2(x))
        x = F.relu(self.b3(x))

        # 2x2
        x = F.relu(self.c1(x))
        x = F.relu(self.c2(x))
        x = F.relu(self.c3(x))

        # 1x128
        x = F.relu(self.d1(x))
        x = F.relu(self.d2(x))
        x = F.relu(self.d3(x))

        x = x.view(-1, 128)
        x = self.last(x)

        # value output
        return torch.tanh(x)