import chess.pgn
import numpy as np
import os
import pickle
import argparse

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
            l[sq] = -board.piece_type_at(sq)
        return [0 if v is None else v for v in l]


def bb2array(b):
    x = np.zeros((12,8,8), dtype=np.int8)
    piece_list = convert_to_int(b)

    for pos, piece in enumerate(piece_list):
        if piece != 0:
            col = int(pos % 8)
            row = int(pos / 8)
            x[piece-1][row][col] = 1

    return x


def yield_board_state(game):
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        board_array = bb2array(board)
        
        yield board_array


def generate_dataset(which_set):
    result_map = {'1-0': 1, '1/2-1/2': 0, '0-1': -1}

    i = 1
    x, y = [], []
    for filename in os.listdir(f"data/{which_set}"):
        if filename.endswith(".pgn"):
            print(f"Reading from {filename}")
            for game in yield_game_from_pgn(open(f"data/{which_set}/{filename}")):
                print(f"Parsing game {i}")
                i += 1
                result = result_map[game.headers['Result']]
                for board in yield_board_state(game):   
                    x.append(board)
                    y.append(result)
                    
    np.savez(f"data/{which_set}/{which_set}.npz", x=x, y=y)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--set', action="store")
    args = parser.parse_args()    
    
    generate_dataset(args.set)
