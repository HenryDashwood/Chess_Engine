class Human:
    def move(self, board):
        choice = int(input())
        row = (choice - 1) // board.board_len
        col = (choice - 1) % board.board_len
        return row, col
