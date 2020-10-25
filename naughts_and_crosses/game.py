from players import Human, Naive


class Board:
    def __init__(self, board_len):
        self.board_len = board_len
        self.layout = [[0] * self.board_len for _ in range(self.board_len)]
        self.cross_turn = False

    def display(self):
        symbols = {"1": "X", "0": " ", "-1": "O"}
        for row in self.layout:
            print([symbols[str(p)] for p in row])

    def place(self, row: int, col: int):
        if not self.layout[row][col]:
            if self.cross_turn:
                self.layout[row][col] = 1
            else:
                self.layout[row][col] = -1
        else:
            print("Place taken, try again")

    def check_win(self):
        diag_vals = [self.layout[i][i] for i in range(self.board_len)]
        if len(set(diag_vals)) == 1 and diag_vals[0]:
            return True
        diag_vals = [self.layout[i][self.board_len - 1] for i in range(self.board_len)]
        if len(set(diag_vals)) == 1 and diag_vals[0]:
            return True

        for row in self.layout:
            if len(set(row)) == 1 and row[0]:
                return True

        for i in range(self.board_len):
            col_vals = [row[i] for row in self.layout]
            if len(set(col_vals)) == 1 and col_vals[0]:
                return True

        return False

    def check_draw(self):
        if 0 not in set([p for row in self.layout for p in row]):
            return True
        return False

    def legal_moves(self):
        legal_moves = []
        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                if self.layout[i][j] == 0:
                    legal_moves.append((i, j))
        return legal_moves


def play(size, noughts, crosses):
    board = Board(3)

    while True:
        board.display()
        if board.cross_turn:
            row, col = crosses.move(board)
        else:
            row, col = noughts.move(board)
        board.place(row=row, col=col)
        board.cross_turn = not board.cross_turn
        if board.check_win():
            board.display()
            print("Game over")
            break
        if board.check_draw():
            board.display()
            print("Draw")
            break


if __name__ == "__main__":
    noughts = Human()
    crosses = Naive()
    play(3, noughts, crosses)

