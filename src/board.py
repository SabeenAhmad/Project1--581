import random
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
    #Functionality: checks if the cell is within the board
    #Parameter: index of the cell
    def in_bounds(self, r, c):
        return 0 <= r < self.length and 0 <= c < self.width #returns True or False

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
    
    '''
    Functionality: used at the very beginning of the game after the user reveals the first cell
    places the mines not in the first cell and its neighbors
    
    Parameters: takes in the index of the user's first move, r,c, how many mines the user wants on the board
    '''
    def place_mine(self,user_r, user_c ,mine_total):
        excluded_cells = self.neighbors(user_r,user_c)
        excluded_cells.append((user_r,user_c))
        while(mine_total > 0):
            r = random.randint(0,9)
            c = random.randint(0,9)
            if(self.is_mine[r][c] == False and (r,c) not in excluded_cells): #checking that index isn't already mine and not user's first move
                self.is_mine[r][c] = True
                mine_total-=1
            else: #if it is user's first move or already a mine
                continue