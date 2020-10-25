import os

import chess
import chess.pgn
import numpy as np


class State(object):
    def __init__(self, board=None):
        if board == None:
            self.board = chess.Board()
        else:
            self.board = board

    def key(self):
        return (
            self.board.board_fen(),
            self.board.turn,
            self.board.castling_rights,
            self.board.ep_square,
        )

    def serialize(self):
        assert self.board.is_valid()

        bstate = np.zeros(64, np.uint8)
        for i in range(64):
            pp = self.board.piece_at(i)
            if pp is not None:
                bstate[i] = {
                    "P": 1,
                    "N": 2,
                    "B": 3,
                    "R": 4,
                    "Q": 5,
                    "K": 6,
                    "p": 9,
                    "n": 10,
                    "b": 11,
                    "r": 12,
                    "q": 13,
                    "k": 14,
                }[pp.symbol()]
        if self.board.has_queenside_castling_rights(chess.WHITE):
            assert bstate[0] == 4
            bstate[0] = 7
        if self.board.has_kingside_castling_rights(chess.WHITE):
            assert bstate[7] == 4
        if self.board.has_queenside_castling_rights(chess.BLACK):
            assert bstate[56] == 12
            bstate[56] = 15
        if self.board.has_kingside_castling_rights(chess.BLACK):
            assert bstate[63] == 12
            bstate[63] = 15
        if self.board.ep_square is not None:
            assert bstate[self.board.ep_square] == 0
            bstate[self.board.ep_square] = 8
        bstate = bstate.reshape(8, 8)

        state = np.zeros((5, 8, 8), np.uint8)

        state[0] = (bstate >> 3) & 1
        state[1] = (bstate >> 2) & 1
        state[2] = (bstate >> 1) & 1
        state[3] = (bstate >> 0) & 1

        state[4] = self.board.turn * 1.0

        return state

    def edges(self):
        return list(self.board.turn * 1.0)


def get_dataset(num_samples=None):
    X, y = [], []
    gn = 0
    values = {"1/2-1/2": 0, "0-1": -1, "1-0": 1}
    for fn in os.listdir("data"):
        pgn = open(os.path.join("data", fn))
        while 1:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            res = game.headers["Result"]
            if res not in values:
                continue
            value = values[res]
            board = game.board()
            for i, move in enumerate(game.mainline_moves()):
                board.push(move)
                ser = State(board).serialize()
                X.append(ser)
                y.append(value)
            print("Parsing game %d, got %d examples" % (gn, len(X)))
            if num_samples is not None and len(X) > num_samples:
                X = np.array(X)
                y = np.array(y)
                return X, y
            gn += 1
    X = np.array(X)
    y = np.array(y)

    return X, y


if __name__ == "__main__":
    X, y = get_dataset(10000)
    print(type(X))
    np.savez("dataset_100.npz", X, y)
