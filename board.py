import chess
import random

class Game():

    def __init__(self):
        self.board = chess.Board()

    def display_board(self, board, use_svg):
        if use_svg:
            return board._repr_svg_()
        else:
            return "<pre>" + str(board) + "</pre>"

    def play_game(self, player1, player2, visual="svg"):
        """
        playerN1, player2: functions that takes board, return uci move
        visual: "simple" | "svg" | None
        """
        use_svg = (visual == "svg")
        board = self.board
        try:
            while not board.is_game_over(claim_draw=True):
                if board.turn == chess.WHITE:
                    uci = player1(board)
                else:
                    uci = player2(board)
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
        if visual is not None:
            print(msg)
        return (result, msg, board)

    def who(self, player):
        return "White" if player == chess.WHITE else "Black"

if __name__ == "__main__":

    def random_player(board):
        move = random.choice(list(board.legal_moves))
        return move.uci()

    game = Game()
    game.play_game(random_player, random_player, visual="print")
