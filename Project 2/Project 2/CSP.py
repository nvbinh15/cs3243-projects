import sys


OBSTACLE = -1
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
        pass

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
        return {(pr, pc):True for (pr, pc) in reachable if (pr >= 0) and (pr < board.rows) and (pc >= 0) and (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE)}
    
    def get_type(self):
        return "King"


class Rook(Piece):

    def get_reachable_position(self, board):
        r, c = self.position
        res = dict()
        pr, pc = r, c 
        while (pr >= 0) and (board.grid[pr][pc] != OBSTACLE):
            res[(pr, pc)] = True
            pr -= 1
        pr = r + 1
        while (pr < board.rows) and (board.grid[pr][pc] != OBSTACLE):
            res[(pr, pc)] = True
            pr += 1
        pr, pc = r, c-1
        while (pc >= 0) and (board.grid[pr][pc] != OBSTACLE):
            res[(pr, pc)] = True
            pc -= 1 
        pc = c + 1 
        while (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE):
            res[(pr, pc)] = True
            pc += 1           
        return res

    def get_type(self):
        return "Rook"


class Bishop(Piece):

    def get_reachable_position(self, board):
        r, c = self.position
        res = dict()
        pr, pc = r, c
        while (pr >= 0) and (pc >= 0) and (board.grid[pr][pc] != OBSTACLE):
            res[(pr, pc)] = True
            pr -= 1
            pc -= 1
        pr, pc = r-1, c+1
        while (pr >= 0) and (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE):
            res[(pr, pc)] = True
            pr -= 1
            pc += 1
        pr, pc = r+1, c-1
        while (pr < board.rows) and (pc >= 0) and (board.grid[pr][pc] != OBSTACLE):
            res[(pr, pc)] = True
            pr += 1
            pc -= 1
        pr, pc = r+1, c+1
        while (pr < board.rows) and (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE):
            res[(pr, pc)] = True
            pr += 1
            pc += 1
        return res

    def get_type(self):
        return "Bishop"


class Knight(Piece):

    def get_reachable_position(self, board):
        r, c = self.position
        reachable = [
            (r-2, c-1), (r-2, c+1), 
            (r-1, c-2), (r-1, c+2),
            (r, c),
            (r+1, c-2), (r+1, c+2),           
            (r+2, c-1), (r+2, c+1)
        ]    
        return {(pr, pc):True for (pr, pc) in reachable if (pr >= 0) and (pr < board.rows) and (pc >= 0) and (pc < board.cols) and (board.grid[pr][pc] != OBSTACLE)}

    def get_type(self):
        return "Knight"


class Queen(Bishop, Rook):

    def get_reachable_position(self, board):
        return {**Rook.get_reachable_position(self, board), **Bishop.get_reachable_position(self, board)}

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

    def __init__(self, board, variables, total_assignments):
        self.board = board 
        self.variables = variables
        self.total_assignments = total_assignments

    def is_valid(self, assignment):
        piece = assignment[-1]
        attacked_positions = piece.get_reachable_position(self.board)
        for p1 in assignment[:-1]:
            if p1.position in attacked_positions:
                return False
        return True

    def is_complete(self, assignment):
        return self.total_assignments == len(assignment)
    

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
    
    board = Board(grid, rows, cols)
    total_assignments = sum(num_pieces)

    variables = {
        "King": num_pieces[0],
        "Queen": num_pieces[1],
        "Bishop": num_pieces[2],
        "Rook": num_pieces[3],
        "Knight": num_pieces[4]
    }
    state = State(board=board, variables=variables, total_assignments=total_assignments)
    return backtrack(state, list())


invalid_records = dict()
var_domain_record = dict()

def backtrack(state, assignment):
    global invalid_records
    global var_domain_record

    if state.is_complete(assignment):
        return {p.get_chess_coord(): p.get_type() for p in assignment}
    
    
    assignment_record = assignment_to_record(assignment)
    if assignment_record not in var_domain_record:
        var_domain_record[assignment_record] = select_unassigned_variable(state, assignment), order_domain_values(state, assignment)
    var, domain = var_domain_record[assignment_record]

    for value in domain:
        piece = Queen(value) if var == 'Queen' else Rook(value) if var == 'Rook' else \
            Bishop(value) if var == 'Bishop' else Knight(value) if var == 'Knight' else King(value)
        assignment.append(piece)
        if forward_check(state, assignment):
            if assignment_to_record(assignment) not in invalid_records and state.is_valid(assignment):
                result = backtrack(state, assignment)
                if result:
                    return result
        invalid_records[assignment_to_record(assignment)] = True
        assignment.pop()
    return None


def forward_check(state, assignment):
    return (state.total_assignments - len(assignment)) <= len(order_domain_values(state, assignment))


def assignment_to_record(assignment):
    record = {t: list() for t in ["King", "Queen", "Bishop", "Rook", "Knight"]}
    for piece in assignment:
        record[piece.get_type()].append(piece.position)
    for key in record:
        record[key] = sorted(record[key])
    return str(record)


def select_unassigned_variable(state, assignment):
    remainder = {type: state.variables[type] for type in state.variables}
    for piece in assignment:
        remainder[piece.get_type()] -= 1
    return "Queen" if remainder["Queen"] > 0 else "Rook" if remainder["Rook"] > 0 else \
        "Bishop" if remainder['Bishop'] > 0 else "Knight" if remainder['Knight'] > 0 else "King"
        
attacked_record = dict()

def order_domain_values(state, assignment):
    global attacked_record

    grid = [row[:] for row in state.board.grid]
    for piece in assignment:
        if (piece.get_type(), piece.position) not in attacked_record:
            attacked_record[(piece.get_type(), piece.position)] = piece.get_reachable_position(state.board)
        attacked = attacked_record[(piece.get_type(), piece.position)]
        for (i,j) in attacked:
            grid[i][j] = OBSTACLE
    return [(i, j) for i in range(state.board.rows) for j in range(state.board.cols) if grid[i][j] != OBSTACLE]
    


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
