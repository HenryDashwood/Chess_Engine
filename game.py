import chess
import random
from IPython.display import display, clear_output

from players import Random, Human

class Game():

    def __init__(self):
        self.board = chess.Board()

    def play_game(self, player1, player2):

        try:
            display(self.board)
            while not self.board.is_game_over(claim_draw=True):
                if self.board.turn == chess.WHITE:
                    uci = player1.move(self.board)
                else:
                    uci = player2.move(self.board)
                self.board.push_uci(uci)
                clear_output(wait=True)
                display(self.board)
        except KeyboardInterrupt:
            msg = "Game interrupted!"
            return (None, msg, self.board)
        result = None
        if self.board.is_checkmate():
            msg = "checkmate: " + self.who(not self.board.turn) + " wins!"
            result = not self.board.turn
        elif self.board.is_stalemate():
            msg = "draw: stalemate"
        elif self.board.is_fivefold_repetition():
            msg = "draw: 5-fold repetition"
        elif self.board.is_insufficient_material():
            msg = "draw: insufficient material"
        elif self.board.can_claim_draw():
            msg = "draw: claim"
        print(self.board.result())
        print(msg)

        return (result, msg, self.board)

    def who(self, player):
        return "White" if player == chess.WHITE else "Black"

if __name__ == "__main__":

    game = Game()
    player1 = Random(game)
    player2 = Random(game)

    game.play_game(player1, player2)
