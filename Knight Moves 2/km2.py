from collections import Counter, deque

# Observations:
# 1. Since we have to visit each region the same amount of times, can't repeat moves, and the size of the smallest region is 5, we can never visit any region >5 times
# 2. Pigeonhole Principle: The number 49 is given to us. Since there are 12 regions and 49/12 > 4, we'll need to visit each region >= 5 times
# 3. Putting observations 1 & 2 together, we need to visit each region exactly 5 times (making 12*5 = 60 moves in total)
# 4. Since there are 10 rows/columns, we need to visit each 60/10 = 6 times

# Given limit (outside) values
topLimit = [None, 29, 19, 33, 20, 27, 36, 35]
bottomLimit = [13, 14, 12, 2, 1, 5, 7, None]
leftLimit = [18, 19, 30, 10, 16, 11, 12, None]
rightLimit = [None, 26, 36, 25, 37, 4, 23, 6]

# Board (as given)
board = [
    [   1, None, None, None, None, None,   43, None, None, None],
    [None, None, None, None, None, None, None, None, None,   13],
    [None,    4, None, None, None, None, None, None, None,   40],
    [None, None,   46, None, None,    7, None, None, None, None],
    [None, None, None, None, None,   16, None, None, None,   10],
    [None, None, None, None,   28, None, None, None,   34,   31],
    [  49, None, None, None, None, None, None, None, None, None],
    [None, None, None,   19, None, None, None, None, None, None],
    [None, None,   25, None, None, None, None, None,   37, None],
    [None, None,   22, None, None, None, None, None, None, None],
]

# Regions (as given)
boardRegions = [
    [1,  1,  1,  1,  2,  2,  2,  2,  2,  2],
    [1,  3,  3,  1,  2,  2,  2,  2,  2,  4],
    [1,  3,  5,  5,  5,  5,  5,  4,  4,  4],
    [1,  3,  3,  5,  5,  5,  5,  5,  6,  4],
    [7,  3,  3,  3,  3,  3,  5,  8,  6,  6],
    [7,  7,  9,  3, 10,  8,  8,  8,  6,  6],
    [7,  9,  9, 11, 10, 10, 10,  8,  8,  8],
    [7,  9, 11, 11, 10, 12, 10,  8, 10, 10],
    [7,  9,  9, 11, 12, 12, 10, 10, 10, 10],
    [7, 11, 11, 11, 11, 12, 12, 10, 10, 10],
]

# Scans the given board to see if we were given the position of a digit ahead of time
def getKnownPosition(digit):
    for r, row in enumerate(board):
        for c, col in enumerate(row):
            if board[r][c] == digit:
                return (r, c)
    return None

# Variable to hold the final solution board
solutionBoard = None

# DFS by placing one incremental digit at each valid location, we'll eventually reach a valid state
def dfs(board, position, regionsVisited, rowsVisited, colsVisited):
    r, c = position

    # See "Observations" section above for why this is a valid way to verify the solution state
    if sum(regionsVisited.values()) == 60:
        global solutionBoard
        solutionBoard = board
        return

    # Neighbors by knight's move
    neighbors = [
        (r-2, c+1),
        (r-1, c+2),
        (r+1, c+2),
        (r+2, c+1),
        (r+2, c-1),
        (r+1, c-2),
        (r-1, c-2),
        (r-2, c-1),
    ]
    
    # Valid moves are neighbors that are within board bounds and are currently empty
    # If the next digit has already been placed on the board (i.e. it was given), make sure we only move to that position
    validMoves = []
    knownNextPosition = getKnownPosition(board[r][c] + 1)
    for row, col in neighbors:
        if knownNextPosition:
            if knownNextPosition == (row, col):
                validMoves.append(knownNextPosition)
                break
        elif row >= 0 and row < len(board) and col >= 0 and col < len(board):
            if boardRegions[row][col] != boardRegions[r][c]:
                if not board[row][col]:
                    validMoves.append((row, col))
    
    # DFS to each valid move as long as it:
    # 1. Moves to a different region of the board
    # 2. Doesn't violate the region, row, or column visit count constraints (see "Observations" section)
    for row, col in validMoves:
        newBoard = [row.copy() for row in board]
        newBoard[row][col] = board[r][c] + 1

        newRegions = regionsVisited.copy()
        newRegions[boardRegions[row][col]] += 1

        newRowsVisited = rowsVisited.copy()
        newRowsVisited[row] += 1

        newColsVisited = colsVisited.copy()
        newColsVisited[col] += 1

        if newRegions[boardRegions[row][col]] <= 5 and newRowsVisited[row] <= 6 and newColsVisited[col] <= 6:
            dfs(newBoard, (row, col), newRegions, newRowsVisited, newColsVisited)

dfs(board, (0, 0), Counter([1]), Counter([0]), Counter([0]))

# Count the product of the size of empty cell groups
# We do this by BFSing from each empty square and counting how many adjacent empty squares there were (multiplying as we go)
def getIslandProduct(board):
    board = [row.copy() for row in board]
    
    def bfs(startRow, startCol):
        bfsq = deque()
        bfsq.append((startRow, startCol))
        size = 0
        while bfsq:
            r, c = bfsq.popleft()

            if r < 0 or c < 0 or r >= len(board) or c >= len(board):
                continue

            if not board[r][c]:
                board[r][c] = 1
                size += 1
                
                bfsq.append((r+1, c))
                bfsq.append((r-1, c))
                bfsq.append((r, c+1))
                bfsq.append((r, c-1))
        return size
    
    islandProducts = None
    for r, row in enumerate(board):
        for c, col in enumerate(row):
            if not board[r][c]:
                bfsSize = bfs(r, c)
                if islandProducts == None:
                    islandProducts = bfsSize
                else:
                    islandProducts *= bfsSize
    
    return islandProducts

# Once we have our working board, calculate the product of the size of empty regions
islandProduct = getIslandProduct(solutionBoard)

print(f"Solution is >> {islandProduct} << from board:")
[print(row) for row in solutionBoard]