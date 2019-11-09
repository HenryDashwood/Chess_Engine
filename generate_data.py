import chess.pgn
import numpy as np
import pickle

pgn = open("data/ficsgamesdb_201901_standard2000_nomovetimes_98589.pgn")

def yield_game_from_pgn(pgn_file):
    while True:
        try:
            game = chess.pgn.read_game(pgn_file)
        except:
            continue

        if not game:
            break

        yield game


def convert_to_int(board):
        l = [None] * 64
        # Check if white
        for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):
            l[sq] = board.piece_type_at(sq)
        # Check if black
        for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):
            l[sq] = 13 - board.piece_type_at(sq)
        return [0 if v is None else v for v in l]



def bb2array(b):
    x = np.zeros((8,8,12), dtype=np.int8)
    piece_list = convert_to_int(b)

    for pos, piece in enumerate(piece_list):
        if piece != 0:
            col = int(pos % 8)
            row = int(pos / 8)
            x[row][col][piece-1] = 1

    return x


def yield_board_state(game):
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        board_array = bb2array(board)

        yield board_array


result_map = {'1-0': 1, '0-1': -1, '1/2-1/2': 0}

x, y = [], []
i = 1
for game in yield_game_from_pgn(pgn):
    print(f"Parsing game {i}")
    i += 1
    result = result_map[game.headers['Result']]
    for board in yield_board_state(game):
        x.append(board)
        y.append(result)
with open('data/board_states.pkl', 'wb') as f:
    pickle.dump(x, f)
with open('data/results.pkl', 'wb') as f:
    pickle.dump(y, f)
