from board import Board

def find_safe_covered_number(board):
    for r in range(board.length):
        for c in range(board.width):
            if (not board.is_mine(r,c) and
                board.state[r][c] == "COVERED" and
                board.adj[r][c] > 0):
                return r,c
    raise RuntimeError("No safe covered number cell found!")

# --- Test 4 ---
print("\n--- Test 4: uncover twice ---")
b = Board(10)
b.uncover(0,0,True)   # place mines + compute adj

r,c = find_safe_covered_number(b)
rc1 = b.uncover(r,c,False)
print("First uncover:", rc1, "state:", b.state[r][c])
rc2 = b.uncover(r,c,False)
print("Second uncover:", rc2, "state:", b.state[r][c])

# --- Test 5 ---
print("\n--- Test 5: uncover flagged ---")
b2 = Board(10)
b2.uncover(0,0,True)

# pick a cell that’s still covered
for r in range(b2.length):
    for c in range(b2.width):
        if b2.state[r][c] == "COVERED":
            test_r, test_c = r,c
            break
    else:
        continue
    break

flag_result = b2.toggle_flag(test_r,test_c)
print(f"Flagging ({test_r},{test_c}):", flag_result, "state:", b2.state[test_r][test_c])

uncover_result = b2.uncover(test_r,test_c,False)
print("Uncover flagged:", uncover_result, "state:", b2.state[test_r][test_c])
