from collections import deque

# Given limit (border) values
topLimit = [None, 29, 19, 33, 20, 27, 36, 35]
bottomLimit = [13, 14, 12, 2, 1, 5, 7, None]
leftLimit = [18, 19, 30, 10, 16, 11, 12, None]
rightLimit = [None, 26, 36, 25, 37, 4, 23, 6]

# Full size board
board = [
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None,    1, None, None, None],
]

# Example (small) board
sTopLimit    = [None, None,    9, None]
sBottomLimit = [None,    1,    4, None]
sLeftLimit   = [   6,    3, None, None]
sRightLimit  = [None, None,    2,    4]
sSolved = [
    [None,    6,    9, None],
    [None,    3, None,    7],
    [   5,    8, None,    2],
    [None,    1,    4, None]
]
sBoard = [
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
    [None,    1, None, None],
]

def isValidBoard(board):
    def isValidLine(expectedFirstDigit, line):
        if not expectedFirstDigit:
            return True
        for num in line:
            if not num:
                continue
            if num and num == expectedFirstDigit:
                return True
            return False
        return True
    
    for r, row in enumerate(board):
        if not isValidLine(leftLimit[r], row):
            return False
        if not isValidLine(rightLimit[r], row[::-1]):
            return False
    
    for colIndex in range(len(board)):
        column = [row[colIndex] for row in board]
        if not isValidLine(topLimit[colIndex], column):
            return False
        if not isValidLine(bottomLimit[colIndex], column[::-1]):
            return False
    return True

def isImpossibleToSolve(board):
    for r, row in enumerate(board):
        if row[0] and leftLimit[r] and row[0] != leftLimit[r]:
            return True
        if row[-1] and rightLimit[r] and row[-1] != rightLimit[r]:
            return True
    for c, col in enumerate(board[0]):
        if col and topLimit[c] and col != topLimit[c]:
            return True
    for c, col in enumerate(board[-1]):
        if col and bottomLimit[c] and col != bottomLimit[c]:
            return True
    return False

def getRowConstraint(value):
    if value in leftLimit:
        return leftLimit.index(value)
    if value in rightLimit:
        return rightLimit.index(value)
    return None
def getColConstraint(value):
    if value in topLimit:
        return topLimit.index(value)
    if value in bottomLimit:
        return bottomLimit.index(value)
    return None

workingBoards = []
def solve(board, position):
    r, c = position

    if isImpossibleToSolve(board):
        return

    if isValidBoard(board):
        workingBoards.append(board)

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

    validMoves = []
    rowConstraint = getRowConstraint(board[r][c]+1)
    colConstraint = getColConstraint(board[r][c]+1)
    for row, col in neighbors:
        if row >= 0 and row < len(board) and col >= 0 and col < len(board):
            if not board[row][col]:
                if (rowConstraint == None or row == rowConstraint) and (colConstraint == None or col == colConstraint):
                    validMoves.append((row, col))
    
    for row, col in validMoves:
        newBoard = [row.copy() for row in board]
        newBoard[row][col] = board[r][c] + 1
        solve(newBoard, (row, col))

solve(board, (7, 4))

print(f"Found {len(workingBoards)} valid boards")

def getIslandProducts(board):
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

# For each working board, calculate the product of the size of empty regions
# Keep track of the lowest product we see
minProduct = float('inf')
minBoard = None
for board in workingBoards:
    islandProduct = getIslandProducts(board)
    if islandProduct < minProduct:
        minProduct = islandProduct
        minBoard = board

print(f"Best result is >> {minProduct} << with board:")
[print(row) for row in minBoard]