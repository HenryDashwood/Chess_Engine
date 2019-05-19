import chess
import random

from ais import Random

class Game():

    def __init__(self):
        self.board = chess.Board()

    def play_game(self, player1, player2):

        board = self.board
        try:
            while not board.is_game_over(claim_draw=True):
                if board.turn == chess.WHITE:
                    uci = player1.move()
                else:
                    uci = player2.move()
                board.push_uci(uci)
                print(self.board)
        except KeyboardInterrupt:
            msg = "Game interrupted!"
            return (None, msg, board)
        result = None
        if board.is_checkmate():
            msg = "checkmate: " + self.who(not board.turn) + " wins!"
            result = not board.turn
        elif board.is_stalemate():
            msg = "draw: stalemate"
        elif board.is_fivefold_repetition():
            msg = "draw: 5-fold repetition"
        elif board.is_insufficient_material():
            msg = "draw: insufficient material"
        elif board.can_claim_draw():
            msg = "draw: claim"
        print(msg)

        return (result, msg, board)

    def who(self, player):
        return "White" if player == chess.WHITE else "Black"

if __name__ == "__main__":

    game = Game()
    player1 = Random(game.board)
    player2 = Random(game.board)

    game.play_game(player1, player2)
