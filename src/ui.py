# UI file
from board import Board
class UI: 
    def __init__(self):
        # Initialize UI with no board yet — will be set in start_screen()
        self.board = None # Stores a reference to the Board object so board.py can be reached.

    def start_screen(self):
        # Functionality: Displays the welcome screen, prompts for valid mine count, then creates the Game and Board and starts rendering.
        # Parameters: (none)
        input("=== Welcome to Minesweeper ===\nPress ENTER to start...")
        while True:
            try:
                mines = int(input("How many mines do you want on the board, must choose between 10-20: "))
                if mines <= 20 and mines >=10:
                    break
                else:
                    print("invalid mine count")
            # Catches anything that isn’t a number
            except:
                print("invalid response")
        # Create a Board object with chosen number of mines
        self.board = Board(mines)
        # Start the game loop
        self.render_board() 

    def end_screen(self):
        # Functionality: Handles game-over flow—prints result, reveals full board, and optionally restarts or exits.
        # Parameters: (none)
        print("\n=== Game Over ===")
        if self.board.playing_state == "WON":
            print("Congratulations, you won!")
        else:
            print("💣 You hit a mine. Better luck next time!")

        # reveal full board at the end
        self.board.print_board("END")

        # ask to play again
        while True:
            again = input("\nDo you want to play again? (y/n): ").strip().lower()
            if again in ("y", "yes"):
                # reset the game
                self.board.playing_state = "PLAYING"
                self.board = Board(self.board.mine_total)
                self.start_screen()
                break
            elif again in ("n", "no"):
                print("Thanks for playing Minesweeper! Goodbye!")
                exit()
            else:
                print("Please enter 'y' or 'n'.")

        # called at the end of render_board()
        # print game over 
        # check if the user won or lost by checking game.playing_state

    def render_status(self): 
        # Functionality: Shows current game stats such as flags remaining, inferred mine count, and game state.
        # Parameters: (none)
        flags_remaining = self.board.flags_remaining
        print(f"Flags remaining: {flags_remaining}")
        mine_count = self.board.mine_total - flags_remaining
        print(f"Mine Count: {mine_count}")
        print(f"Game State: {self.board.playing_state}")
    def render_board(self): 
        # Functionality: Main game loop—renders status and board, accepts moves, updates state, and detects win/loss.
        # Parameters: (none)
        print("\n--- Game started! ---")

        first_move = True
        while self.board.playing_state == "PLAYING":
            self.render_status()
            self.board.print_board("PLAYING")

            # ask player for move
            action, row, col = self.ask_for_input()

            if action == "reveal":
                result = self.board.uncover(row, col, first_move)
                first_move = False
                if result == "HIT":
                    self.board.playing_state = "LOST"
                elif result == "SAFE":
                    if self.board.check_win():
                        self.board.playing_state = "WON"
                elif result == "FLAGGED":
                    print("That cell is flagged, remove flag first.")
                elif result == "REVEALED":
                    print("That cell is already revealed.")

            elif action == "flag":
                result = self.board.toggle_flag(row, col)
                if result == "FLAGGED":
                    print(f"Flag placed at {chr(col + 65)}{row + 1}")
                elif result == "UNFLAGGED":
                    print(f"Flag removed at {chr(col + 65)}{row + 1}")
                elif result == "NO_FLAGS":
                    print("No flags remaining!")
                elif result == "INVALID":
                    print("Cannot flag this cell!")

        # when loop ends → game over
        self.end_screen()

    def ask_for_input(self): 
        # Functionality: Validates and parses user input into an action ('reveal'/'flag') and board coordinates.
        # Returns: (action, row, col) tuple when input is valid.
        # Parameters: (none)
        # loop to continue asking the user for valid input
        while True:
            # asks for user input, case insensitive and removes leading/trailing whitespace
            user_input = input("\nEnter move (e.g. 'reveal A5' or 'flag B3', or 'quit' to exit): ").strip().lower()
            # if user presses enter on input request, loop to ask again 
            if not user_input:
                continue
            # if user wants to quit
            if user_input == "quit":
                print("Thanks for playing!")
                exit()
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
                
            #valid volumns
            columns = "ABCDEFGHIJ"
            if position[0].upper() not in columns:
                print("Invalid column - use A-J")
                continue
            # finds the index of the user input row
            col = columns.index(position[0].upper())
            row_num = int(position[1:])
            if not (1 <= row_num <= 10):
                print("Invalid row - use 1-10")
                continue
            row = row_num - 1
            # calls upon in_bounds function from board.py to check input and loop again if input is incorrect
            if not self.board.in_bounds(row, col):
                print("Invalid input - Out of bounds")
                continue 
            # if all checks pass, pass along input to render_board()
            return action, row, col
