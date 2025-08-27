class Board:
    def __init__ (self, mine_total):
        self.width = 10
        self.length = 10
        self.board = [["." for x in range(10)] for _ in range(10)]
    
    def print_board(self, playing_state):
        cell_width = 3  # every column (including headers) takes 3 spaces

        # column headers (A–J)
        print(" " * cell_width, end="")   # top-left empty corner
        for c in range(10):
            col_letter = chr(ord("A") + c)
            print(f"{col_letter:>{cell_width}}", end="")
        print()

        # rows (1–10)
        for r in range(10):
            print(f"{r+1:>{cell_width}}", end="")  # row label
            for c in range(10):
                if playing_state == 'PLAYING':
                    ch = self.board[r][c]
                else:
                    ch = "."
                print(f"{ch:>{cell_width}}", end="")
            print()



