import random
from collections import deque

class Board:
    def __init__ (self, mine_total):
        self.width = 10
        self.length = 10
        self.mines = [[False]*self.width for _ in range(self.length)]
        self.state   = [["COVERED"]*self.width for _ in range(self.length)]
        self.adj     = [[0]*self.width for _ in range(self.length)]
        self.mine_total = mine_total

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
    def place_mine(self,user_r, user_c ):
        mine_count = self.mine_total
        excluded_cells = self.neighbors(user_r,user_c)
        excluded_cells.append((user_r,user_c))
        while(mine_count > 0):
            r = random.randint(0,9)
            c = random.randint(0,9)
            if(self.mines[r][c] == False and (r,c) not in excluded_cells): #checking that index isn't already mine and not user's first move
                self.mines[r][c] = True
                mine_count-=1
            else: #if it is user's first move or already a mine
                continue
    '''
    Functionality: returns whether cell is mine
    Parameters: cell's row and column
    '''
    def is_mine(self,r,c):
        return self.mines[r][c] == True
        '''
    Functionality: returns whether cell is flag
    Parameters: cell's row and column
    '''
    def is_flag(self,r,c):
        return self.state[r][c] == 'FLAG'
        '''
    Functionality: returns whether cell is already uncovered
    Parameters: cell's row and column
    '''
    def is_uncovered(self,r,c):
        return self.state[r][c] == 'UNCOVERED'
    '''
    Functionality: Uncovers the cell, given that it is a valid move(not already uncovered, not a flag)
    Parameters: cell's row and column, if it is the first move
    '''
    def uncover(self,r,c,first_move):
        #if it is the first move, need to place mines, compute neighbors, and fill zeroes where needed
        #returns SAFE to tell game that this was a valid move
        if first_move:
           self.place_mine(r,c)
           self.compute_numbers()
           self.state[r][c] = 'UNCOVERED'
           if self.adj[r][c] == 0:
                self.fill_zeroes(r,c)
           return 'SAFE'
        #if it is not the first move
        else:
            #if it is a flag, tells Game to ask user to either enter a diff cell or remove flag
            if self.is_flag(r,c):
                return 'FLAGGED'
            #if already uncovered, tells Game to ask user to redo
            elif self.is_uncovered(r,c):
                return 'REVEALED'
            #check if mine, return HIT to tell game to end the game
            elif self.is_mine(r,c):
                return 'HIT'
            #if it is a valid cell, returns SAFE to tell game this was a valid move
            else:
                self.state[r][c] = 'UNCOVERED'
                if self.adj[r][c] == 0:
                    self.fill_zeroes(r,c)
                return 'SAFE'

    def fill_zeroes(self,r,c): 
        """
        Functionality: Uses BFS (queue) to uncover a connected region of tiles with zero mines as neighbors and their border numbers.
        Parameters: cell's row and column
        """
        if self.mines[r][c]:
            return

        if self.state[r][c] != 'UNCOVERED':
            self.state[r][c] = 'UNCOVERED'
        #The 2 cases above should be handled by uncover, but I added for more robustness

        # Standard BFS
        q = deque()
        visited = set()
        q.append((r, c))
        visited.add((r, c))

        while q:
            cr, cc = q.popleft()
            if self.adj[cr][cc] != 0:
                continue
            for rr, cc2 in self.neighbors(cr, cc):
                if (rr, cc2) in visited:
                    continue
                if self.mines[rr][cc2]:
                    continue
                visited.add((rr, cc2))
                self.state[rr][cc2] = 'UNCOVERED'
                if self.adj[rr][cc2] == 0:
                    q.append((rr, cc2))