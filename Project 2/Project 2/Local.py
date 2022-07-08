import sys
import random

OBSTACLE = -1
ATTACKED = -2
random_seed = 0
# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################

class Piece:

    def __init__(self, position):
        self.position = position

    def get_chess_coord(self):
        return to_chess_coord(self.position)

    def get_type(self):
        return ""

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
    
    def get_type(self):
        return "King"


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

    def get_type(self):
        return "Rook"


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

    def get_type(self):
        return "Bishop"


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

    def get_type(self):
        return "Knight"


class Queen(Bishop, Rook):

    def get_reachable_position(self, board):
        return list(set(Rook.get_reachable_position(self, board) + Bishop.get_reachable_position(self, board)))

    def get_type(self):
        return "Queen"


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

    def __init__(self, board, pieces):
        self.board = board 
        self.pieces = pieces
        self.degree = dict()

    def value(self):
        self.degree = dict()

        for p in self.pieces:
            attacked_positions = p.get_reachable_position(self.board)
            for p1 in self.pieces:
                if p1 != p and p1.position in attacked_positions:
                    if p in self.degree:
                        self.degree[p] += 1
                    else:
                        self.degree[p] = 1
                    if p1 in self.degree:
                        self.degree[p1] += 1
                    else:
                        self.degree[p1] = 1
        
        return -sum(self.degree.values())

    def assign_best_successor(self):
        if random.random() > random_seed:
            self.pieces.remove(max(self.degree, key=self.degree.get))
        else:
            self.pieces.remove(random.choice(list(self.degree.keys())))
    

#############################################################################
######## Helping Functions
#############################################################################
def to_chess_coord(position):
    (r, c) = position
    return (chr(c+97), r)


#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, pieces, k):

    global random_seed
    piece_objects = list()
    k = int(k)

    for pos, piece in pieces.items():
        if piece == 'King':
            piece_objects.append(King(pos))
        elif piece == 'Rook':
            piece_objects.append(Rook(pos))
        elif piece == 'Bishop':
            piece_objects.append(Bishop(pos))
        elif piece == 'Queen':
            piece_objects.append(Queen(pos))
        elif piece == 'Knight':
            piece_objects.append(Knight(pos))

    board = Board(grid=grid, rows=rows, cols=cols)

    while True:
        state = State(board=board, pieces=piece_objects.copy())
        is_local_maxima = False

        while (len(state.pieces) >= k) and (not is_local_maxima):
            value = state.value()
            state.assign_best_successor()
            if state.value() == 0:
                return {p.get_chess_coord(): p.get_type() for p in state.pieces}
            if state.value() < value or len(state.pieces) <= k:
                is_local_maxima = True
                random_seed = 0.1


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
    k = 0
    pieces = {}

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    k = handle.readline().split(":")[1] # Read in value of k

    piece_nums = get_par(handle.readline()).split()
    num_pieces = 0
    for num in piece_nums:
        num_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        pieces[coords] = piece    

    return rows, cols, grid, pieces, k

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
def run_local():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, pieces, k = parse(testcase)
    goalstate = search(rows, cols, grid, pieces, k)
    return goalstate #Format to be returned
