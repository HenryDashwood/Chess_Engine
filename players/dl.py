import chess
import numpy as np
import torch
from state import State
from train import Net

class DeepLearning:
    def __init__(self):
        vals = torch.load("model.pth", map_location=lambda storage, loc:storage)
        self.model = Net()
        self.model.load_state_dict(vals)

    def move(self, board):
        state = State(board).serialize()
        state = np.expand_dims(state, axis=0)
        state = torch.FloatTensor(state)
        output = self.model(state)
        print(output)
        # print(output.uci())
        return output.uci()
