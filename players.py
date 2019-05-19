import chess
import random

class Classic:

    def __init__(self, game):
        self.game = game

    def move(self):
        raise NotImplementedError

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
