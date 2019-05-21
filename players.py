import chess
import random

class Classic:

    def __init__(self, game):
        self.game = game
        self.MAXVAL = 10000
        self.values = {chess.PAWN:1,chess.KNIGHT:3,chess.BISHOP:3,chess.ROOK:5,chess.QUEEN:9,chess.KING:0}

    def move(self):
        raise NotImplementedError

    def score(self):
        if self.board.is_game_over():
            if self.board.result() == "1-0":
                return self.MAXVAL
            elif self.board.result() == "0-1":
                return -self.MAXVAL
            else:
                return 0

        score = 0.0
        piece_map = self.game.board.piece_map()
        for x in piece_map:
            piece_value = self.values[piece_map[x].piece_type]
            if piece_map[x].color == chess.WHITE:
                score += piece_value
            else:
                score -= piece_value

        actual_turn = self.board.turn
        self.board.turn = chess.WHITE
        score += 0.1 * self.board.legal_moves.count()
        self.board.turn = chess.BLACK
        score -= 0.1 * self.board.legal_moves.count()
        self.board.turn = actual_turn

        return score

class Human:

    def __init__(self, game):
        self.game = game

    def move(self):
        uci = self.get_move("%s's move [q to quit]> " % self.game.who(self.game.board.turn))
        legal_uci_moves = [move.uci() for move in self.game.board.legal_moves]
        while uci not in legal_uci_moves:
            print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
            uci = self.get_move("%s's move[q to quit]> " % self.game.who(self.game.board.turn))
        return uci

    def get_move(self, prompt):
        move = input(prompt)
        if move and move[0] == "q":
            raise KeyboardInterrupt()
        try:
            chess.Move.from_uci(move)
        except:
            move = None
        return move

class Random:

    def __init__(self, game):
        self.game = game

    def move(self):
        move = random.choice(list(self.game.board.legal_moves))
        return move.uci()
