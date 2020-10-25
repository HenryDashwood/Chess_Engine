import chess


class Human:
    def move(self, board):
        uci = self.get_move("Your move: ")
        legal_uci_moves = [move.uci() for move in board.legal_moves]
        while uci not in legal_uci_moves:
            print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
            uci = self.get_move("%s's move[q to quit]>" % board.who(board.turn))
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
