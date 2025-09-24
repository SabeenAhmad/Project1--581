import random
from collections import deque

class Board:
    def __init__ (self, mine_total, difficulty):
        # Functionality: Initializes the board with given size, mine count, and default states for cells.
        self.width = 10
        self.length = 10
        self.mines = [[False]*self.width for _ in range(self.length)]
        self.state   = [["COVERED"]*self.width for _ in range(self.length)] # COVERED, FLAG, UNCOVERED
        self.adj     = [[0]*self.width for _ in range(self.length)] # cell number
        self.mine_total = mine_total
        self.playing_state = True
        self.flags_remaining = mine_total
        self.mines_initialized = False
        self.playing_state = "PLAYING"   # can be "PLAYING", "WON", "LOST"
        self.difficulty = difficulty # can be "EASY", "MEDIUM", "HARD"


    def print_board(self, playing_state):
        # Functionality: Prints the current state of the board to the console, showing covered tiles, flags, numbers, or mines.
        # Parameter: playing_state - indicates whether the game is in progress ('PLAYING') or finished (reveals all cells).
        cell_width = 3

        # column headers (A–J)
        print()
        print(" " * cell_width, end="")   # top-left empty corner
        for c in range(self.width):
            col_letter = chr(ord("A") + c)
            print(f"{col_letter:>{cell_width}}", end=" ")
        print()

        # rows (1–10)
        print()
        for r in range(self.length):
            print(f"{r+1:>{cell_width}}", end="")  # row label
            for c in range(self.width):
                if playing_state == 'PLAYING':
                    # While playing, covered cells are hidden, flags show, uncovered shows numbers/empties
                    if self.state[r][c] == "COVERED":
                        ch = "🟢" # covered tile
                    elif self.state[r][c] == "FLAG":
                        ch = "  ⛳️" # flagged tile
                    elif self.state[r][c] == "UNCOVERED":
                        if self.is_mine(r, c):
                            ch = "  💣"   # should never show during play, but just in case
                        else:
                            if self.adj[r][c] > 0: 
                                ch = f"  {self.adj[r][c]} "                            
                            else: 
                                ch = " 🟤"
                    else:
                        ch = "?"
                else:
                    # end state → reveal everything
                    if self.mines[r][c]:
                        ch = "  💣"
                    else:
                        if self.adj[r][c] > 0: 
                            ch = f"  {self.adj[r][c]} "
                        else:  
                            ch = " 🟤"
                print(f"{ch:>{cell_width}}", end="")
            print()
            print()

    def in_bounds(self, r, c):
    # Functionality: Checks if the given cell position is within the dimensions of the board.
    # Parameters: r (row index), c (column index).
    # Returns: True if the cell is inside the board, otherwise False.
        return 0 <= r < self.length and 0 <= c < self.width

    def neighbors(self, r, c):
        # Functionality: Finds all valid neighboring cells around a given cell (up to 8 possible neighbors).
        # Parameters: r (row index), c (column index).
        # Returns: A list of (row, column) tuples for all in-bound neighbors.
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
    
    Parameters: user_r, user_c (row/col of the first click), uses self.mine_total
    '''
    def place_mine(self,user_r, user_c ):
        mine_count = self.mine_total
        excluded_cells = self.neighbors(user_r,user_c)
        excluded_cells.append((user_r,user_c))
        while(mine_count > 0):
            r = random.randint(0,9)
            c = random.randint(0,9)
            # make sure cell isn’t excluded and isn’t already a mine
            if(self.mines[r][c] == False and (r,c) not in excluded_cells): 
                self.mines[r][c] = True
                mine_count-=1
            else:
                continue
    """
    Compute numbers for all cells based on adjacent mines.
    Updates self.adj so self.adj[r][c] = number of surrounding mines.
    """
    def compute_numbers(self):
        for r in range(self.length):
            for c in range(self.width):
                if self.mines[r][c]:
                    self.adj[r][c] = -1  
                else:
                    count = 0
                    for rr, cc in self.neighbors(r, c):
                        if self.mines[rr][cc]:
                            count += 1
                    self.adj[r][c] = count

    '''
    Functionality: returns whether cell is mine
    Parameters: cell's row and column
    '''
    def is_mine(self,r,c):
        # check if cell has a mine
        return self.mines[r][c] == True
    '''
    Functionality: returns whether cell is flag
    Parameters: cell's row and column
    '''
    def is_flag(self,r,c):
        # check if cell is flagged
        return self.state[r][c] == 'FLAG'
    '''
    Functionality: returns whether cell is already uncovered
    Parameters: cell's row and column
    '''
    def is_uncovered(self,r,c):
        # check if cell is uncovered
        return self.state[r][c] == 'UNCOVERED'
    '''
    Functionality: returns whether cell is already covered
    Parameters: cell's row and column
    '''
    def is_covered(self,r,c):
        # check if cell is covered
        return self.state[r][c] == 'COVERED'
    '''
    Functionality: Uncovers the cell, given that it is a valid move(not already uncovered, not a flag)
    Parameters: cell's row and column, if it is the first move
    '''
    def uncover(self, r, c, first_move):
    # Always prevent uncovering flagged cells
        if self.is_flag(r, c):
            return 'FLAGGED'

        # initialize mines on first actual uncover
        if not self.mines_initialized:
            self.place_mine(r, c)
            self.compute_numbers()
            self.mines_initialized = True

        #ifirst move, mines were just placed excluding (r,c); uncover & expand zeros if needed
        if first_move:
            self.state[r][c] = 'UNCOVERED'
            if self.adj[r][c] == 0:
                self.fill_zeroes(r, c)
            return 'SAFE'
        #if it is not the first move
        else:
            #if already uncovered, tells Game to ask user to redo
            if self.is_uncovered(r, c):
                return 'REVEALED'
            #check if mine, return HIT to tell game to end the game
            elif self.is_mine(r, c):
                return 'HIT'
            #if it is a valid cell, returns SAFE to tell game this was a valid move
            else:
                self.state[r][c] = 'UNCOVERED'
                if self.adj[r][c] == 0:
                    self.fill_zeroes(r, c)
                return 'SAFE'

    def check_win(self):
        """
        Player wins if all non-mine cells are uncovered.
        """
        for r in range(self.length):
            for c in range(self.width):
                if not self.mines[r][c] and self.state[r][c] != "UNCOVERED":
                    return False
        return True
        
    def fill_zeroes(self,r,c): 
        """
        Functionality: Uses BFS (queue) to uncover a connected region of tiles with zero mines as neighbors and their border numbers.
        Parameters: cell's row and column
        """
        if self.state[r][c] == 'FLAG' or self.mines[r][c]:
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
                if self.state[rr][cc2] == 'FLAG':
                    continue
                visited.add((rr, cc2))
                self.state[rr][cc2] = 'UNCOVERED'
                # keep expanding if neighbor is also zero
                if self.adj[rr][cc2] == 0:
                    q.append((rr, cc2))
 

    def toggle_flag(self, r, c):
        """
        Functionality: Toggles a flag on a covered cell. If flagged, it unflags; if covered, it flags (unless no flags remain).
        Parameters: cell's row and column
        Returns: 'FLAGGED', 'UNFLAGGED', 'INVALID', or 'NO_FLAGS' depending on the action taken
        """
        if not self.in_bounds(r, c):
            return 'INVALID'

        cell_state = self.state[r][c]

        # cannot flag an uncovered cell
        if cell_state == 'UNCOVERED':
            return 'INVALID'

        # unflag
        if cell_state == 'FLAG':
            self.state[r][c] = 'COVERED'
            self.flags_remaining += 1
            return 'UNFLAGGED'
        
        # place flag
        if self.flags_remaining == 0:
            return 'NO_FLAGS'

        self.state[r][c] = 'FLAG'
        self.flags_remaining -= 1
        return 'FLAGGED'

    """
    Functionality: The AI randomly selects an covered cell (not flagged) and uncovers it for the user.
    Parameters: N/A
    """
    def easy_ai_mode(self):
        uncovered_cells = [] # List of all covered cells to select from
        for r in range(self.length):
            for c in range(self.width):
                if self.is_covered(r, c):
                    # Iterates through all cells and adds the ones that are covered
                    uncovered_cells.append((r, c))
        
        # Check if there are any uncovered cells left
        if not uncovered_cells:
            return "NO_MOVES"

        cell_index = random.randint(0, len(uncovered_cells)) # Randomly selects a cell to uncover
        selected_r = uncovered_cells[cell_index][0]
        selected_c = uncovered_cells[cell_index][1]

        return self.uncover(selected_r, selected_c, False) # Calls uncover function to uncover selected cell    
    
    """
    Functionality: Placeholder for Medium AI code.
    Parameters: N/A
    """
    def medium_ai_mode(self):
        print("Medium AI Mode Selected - Not Yet Implemented")
        return "NO_MOVES"
    
    """
    Functionality: Placeholder for Hard AI code.
    parameters: N/A
    """
    def hard_ai_mode(self):
        print("Hard AI Mode Selected - Not Yet Implemented")
        return "NO_MOVES"
    
    """
    Functionality: This will iterate through the board and find the first cell that is covered and a 0 safe cell.
    It will return this as the hint.
    Parameters: N/A.
    """
    def generate_hint(self):
        columns = "ABCDEFGHIJ" # All the possible columns to index from to give the hint.
        all_safe_cells = [] # Stores all the cells that have a 0.
        for r in range(self.length): # Iterate through each cell of the board.
            for c in range(self.length):
                if self.is_uncovered(r,c) == False and self.adj[r][c] == 0: # Check if it is a covered or flagged cell and it is a cell with 0 adjacent mines.
                    all_safe_cells.append((r+1, columns[c])) # This is a safe cell then.
        rand_safe_cell = random.choice(all_safe_cells) # Choose a random safe cell to give the hint to.
        print(f"Your Hint: A Safe Cell is Located in {rand_safe_cell[1]}{rand_safe_cell[0]}") # Print the hint message.