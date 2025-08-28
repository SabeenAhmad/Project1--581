class Board:
    def __init__ (self, mine_total):
        self.width = 10
        self.length = 10
        self.is_mine = [[False]*self.width for _ in range(self.length)]
        self.state   = [["COVERED"]*self.width for _ in range(self.length)]
        self.adj     = [[0]*self.width for _ in range(self.length)]

    def print_board(self, playing_state):
        cell_width = 3  # every column (including headers) takes 3 spaces

        # column headers (A–J)
        print(" " * cell_width, end="")   # top-left empty corner
        for c in range(self.width):
            col_letter = chr(ord("A") + c)
            print(f"{col_letter:>{cell_width}}", end="")
        print()

        # rows (1–10)
        for r in range(self.length):
            print(f"{r+1:>{cell_width}}", end="")  # row label
            for c in range(self.width):
                if playing_state == 'PLAYING':
                    ch = "." if self.state[r][c] == "COVERED" else self.state[r][c][0]
                else:
                    ch = "."
                print(f"{ch:>{cell_width}}", end="")
            print()

def in_bounds(self, r, c):
    return 0 <= r < self.length and 0 <= c < self.width

def neighbors(self, r, c):
    nbrs = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if self.in_bounds(rr, cc):
                nbrs.append((rr, cc))
    return nbrs




