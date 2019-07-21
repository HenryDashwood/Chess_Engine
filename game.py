import chess
import random
from IPython.display import display, clear_output

from players import Naive, Human, Minimax, MCTS, DeepLearning

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
                print()
            clear_output(wait=True)
            return self.board
        except KeyboardInterrupt:
            print("Game interrupted!")
            return None

if __name__ == "__main__":
    game = Game()
    player1 = Naive()
    player2 = DeepLearning()

    board = game.play_game(player1, player2)
    print(board.result())
