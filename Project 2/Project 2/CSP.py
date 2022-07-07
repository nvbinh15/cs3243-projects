import sys

OBSTACLE = -1
ATTACKED = -2
# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################

class Piece:

    def __init__(self, position):
        self.position = position

    def get_reachable_position(self, board):
        pass


class King(Piece):
    
    def get_reachable_position(self, board):
        r, c = self.position
        reachable = [
            (r-1, c-1), (r-1, c), (r-1, c+1),
            (r, c-1), (r, c), (r, c+1),
            (r+1, c-1), (r+1, c), (r+1, c+1)
        ]
        res = list()
        for pos in reachable:
            pr, pc = pos
            if (pr >= 0) and (pr < board.rows) and (pc >= 0) and (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE):
                res.append(pos)
        return res


class Rook(Piece):

    def get_reachable_position(self, board):
        r, c = self.position
        res = list()
        pr, pc = r, c 
        while (pr >= 0) and (board.grid[pr][pc] != OBSTACLE):
            res.append((pr, pc))
            pr -= 1
        pr = r + 1
        while (pr < board.rows) and (board.grid[pr][pc] != OBSTACLE):
            res.append((pr, pc))
            pr += 1
        pr, pc = r, c-1
        while (pc >= 0) and (board.grid[pr][pc] != OBSTACLE):
            res.append((pr, pc))
            pc -= 1 
        pc = c + 1 
        while (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE):
            res.append((pr, pc))
            pc += 1           
        return res


class Bishop(Piece):

    def get_reachable_position(self, board):
        r, c = self.position
        res = list()
        pr, pc = r, c
        while (pr >= 0) and (pc >= 0) and (board.grid[pr][pc] != OBSTACLE):
            res.append((pr, pc))
            pr -= 1
            pc -= 1
        pr, pc = r-1, c+1
        while (pr >= 0) and (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE):
            res.append((pr, pc))
            pr -= 1
            pc += 1
        pr, pc = r+1, c-1
        while (pr < board.rows) and (pc >= 0) and (board.grid[pr][pc] != OBSTACLE):
            res.append((pr, pc))
            pr += 1
            pc -= 1
        pr, pc = r+1, c+1
        while (pr < board.rows) and (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE):
            res.append((pr, pc))
            pr += 1
            pc += 1
        return res


class Knight(Piece):

    def get_reachable_position(self, board):
        r, c = self.position
        res = list()
        reachable = [
            (r-2, c-1), (r-2, c+1), 
            (r-1, c-2), (r-1, c+2),
            (r, c),
            (r+1, c-2), (r+1, c+2),           
            (r+2, c-1), (r+2, c+1)
        ]    
        for pos in reachable:
            pr, pc = pos
            if (pr >= 0) and (pr < board.rows) and (pc >= 0) and (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE):
                res.append(pos)
        return res


class Queen(Bishop, Rook):

    def get_reachable_position(self, board):
        return list(set(Rook.get_reachable_position(self, board) + Bishop.get_reachable_position(self, board)))


#############################################################################
######## Board
#############################################################################
class Board:
    
    def __init__(self, grid, rows, cols):
        self.grid = grid
        self.rows = rows
        self.cols = cols


#############################################################################
######## State
#############################################################################
class State:

    def __init__(self, board, position, enemy):
        self.board = board 
        self.position = position

        for p, pos in enemy:
            if p == 'King':
                piece = King(pos)
            elif p == 'Rook':
                piece = Rook(pos)
            elif p == 'Bishop':
                piece = Bishop(pos)
            elif p == 'Knight':
                piece = Knight(pos)
            elif p == 'Queen':
                piece = Queen(pos)

            for r, c in piece.get_reachable_position(board):
                board.grid[r][c] = ATTACKED

    def is_valid_state(self, r, c):
        return (r >= 0) and (r < self.board.rows) and (c >= 0) and (c < self.board.cols) and (self.board.grid[r][c] >= 0)
    

#############################################################################
######## Helping Functions
#############################################################################
def to_chess_coord(position):
    (r, c) = position
    return (chr(c+97), r)
#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, num_pieces):
    pass


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))
    cols = int(get_par(handle.readline()))
    grid = [[0 for j in range(cols)] for i in range(rows)]

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    piece_nums = get_par(handle.readline()).split()
    num_pieces = [int(x) for x in piece_nums] #List in the order of King, Queen, Bishop, Rook, Knight

    return rows, cols, grid, num_pieces

def add_piece( comma_seperated):
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r,c), piece]

#Returns row and col index in integers respectively
def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, num_pieces = parse(testcase)
    goalstate = search(rows, cols, grid, num_pieces)
    return goalstate #Format to be returned
