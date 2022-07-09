import sys
import heapq

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
def search(rows, cols, grid, enemy_pieces, own_pieces, goals):

    def heuristic(position, goals):
        r, c = position
        min_manhattan_distance = float('inf')
        for goal in goals:
            if abs(goal[0]-r) + abs(goal[1]-c) < min_manhattan_distance:
                min_manhattan_distance = abs(goal[0]-r) + abs(goal[1]-c)
        return min_manhattan_distance
        
    def is_goal(position, goals):
        r, c = position
        for goal in goals:
            if r == goal[0] and c == goal[1]:
                return True
        return False
    
    board = Board(grid=grid, rows=rows, cols=cols)
    state = State(board=board, position=own_pieces[0][1], enemy=enemy_pieces)

    is_found = False
    reached = {state.position: [0, None]} # key: position, value: [cost, parent]
    frontier = [[0 + heuristic(state.position, goals), 0, state.position]] # [cost + heuristic, cost, position]

    while frontier:
        _, cost, vertex = heapq.heappop(frontier)
        if is_goal(vertex, goals):
            is_found = True
            break
        r, c = vertex
        neighbors = [
            (r-1, c-1), (r-1, c), (r-1, c+1),
            (r, c-1), (r, c+1),
            (r+1, c-1), (r+1, c), (r+1, c+1)
        ]
        for pos in neighbors:
            pr, pc = pos
            if (state.is_valid_state(pr, pc) and (pos not in reached)) or ((pos in reached) and reached[pos][0] > cost + state.board.grid[pr][pc]):
                reached[pos] = [cost + state.board.grid[pr][pc], vertex]
                heapq.heappush(frontier, [cost + state.board.grid[pr][pc] + heuristic((pr, pc), goals), cost + state.board.grid[pr][pc], pos])
    
    if not is_found:
        return [], 0
        
    moves = list()
    child = vertex
    while True:
        if not reached[child][1]:
            break
        moves.append([to_chess_coord(reached[child][1]), to_chess_coord(child)])
        child = reached[child][1]

    return list(reversed(moves)), cost


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline())) # Integer
    cols = int(get_par(handle.readline())) # Integer
    grid = [[1 for j in range(cols)] for i in range(rows)] # Dictionary, label empty spaces as 1 (Default Step Cost)
    enemy_pieces = [] # List
    own_pieces = [] # List
    goals = [] # List

    handle.readline()  # Ignore number of obstacles
    for ch_coord in get_par(handle.readline()).split():  # Init obstacles
        r, c = from_chess_coord(ch_coord)
        grid[r][c] = -1 # Label Obstacle as -1

    handle.readline()  # Ignore Step Cost header
    line = handle.readline()
    while line.startswith("["):
        line = line[1:-2].split(",")
        r, c = from_chess_coord(line[0])
        grid[r][c] = int(line[1]) if grid[r][c] == 1 else grid[r][c] #Reinitialize step cost for coordinates with different costs
        line = handle.readline()
    
    line = handle.readline() # Read Enemy Position
    while line.startswith("["):
        line = line[1:-2]
        piece = add_piece(line)
        enemy_pieces.append(piece)
        line = handle.readline()

    # Read Own King Position
    line = handle.readline()[1:-2]
    piece = add_piece(line)
    own_pieces.append(piece)

    # Read Goal Positions
    for ch_coord in get_par(handle.readline()).split():
        r, c = from_chess_coord(ch_coord)
        goals.append((r, c))
    
    return rows, cols, grid, enemy_pieces, own_pieces, goals

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [piece, (r,c)]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)
    
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_AStar():
    testcase = sys.argv[1]
    rows, cols, grid, enemy_pieces, own_pieces, goals = parse(testcase)
    moves, pathcost = search(rows, cols, grid, enemy_pieces, own_pieces, goals)
    return moves, pathcost
    