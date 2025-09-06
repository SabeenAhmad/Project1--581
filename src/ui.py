# UI file

class UI: 
    def __init__(self, game, board):
        self.game = game # Stores a reference to the Game object so game.py can be reached.
        self.board = board # Stores a reference to the Board object so board.py can be reached.

    def start_screen(self):
        pass

    def ask_for_input(): 
        # loop to continue asking the user for valid input
        while True:
            # asks for user input, case insensitive and removes leading/trailing whitespace
            user_input = input("\nEnter move (e.g. 'reveal A5' or 'flag B3'): ").strip().lower()
            # if user presses enter on input request, loop to ask again 
            if not user_input:
                continue
            # if user's input has too many or too few words, loop to ask again; turn user_input into an array of two elements
            parts = user_input.split()
            if len(parts) != 2:
                print("Invalid input - Type 'reveal A5' or 'flag B3'")
                continue
            # split up the array parts where the first index is called action and the second is position
            action, position = parts
            # if invalid user input, loop to ask again
            if action not in ("reveal", "flag"):
                print("Invalid action -  Use 'reveal' or 'flag'")
                continue
            # if the specified position doesn't begin with a letter and conclude with a digit, loop to ask again 
            if not (len(position) >= 2 and position[0].isalpha() and position[1:].isdigit()):
                print("Invalid position - Type the letter then the number  like 'A5'")
                continue
                
            columns = "ABCDEFGHIJ"
            # finds the index of the user input row
            col = columns.index(position[0].upper())
            # grabs the digit from the user input (the first index would be the letter)
            row = int(position[1:]) - 1
            
            # calls upon in_bounds function from board.py to check input and loop again if input is incorrect
            if not self.board.in_bounds
                print("Invalid input - Out of bounds")
                continue 
            # if all checks pass, pass along input to render_board()
            return action, row, col


    
