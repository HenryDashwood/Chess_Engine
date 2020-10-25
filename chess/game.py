import chess
from IPython.display import clear_output, display

from .players import MCTS, DeepLearning, Human, Minimax, Naive


class Game:
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
    player1 = Minimax(2)
    player2 = Minimax(2)

    board = game.play_game(player1, player2)
    print(board.result())
