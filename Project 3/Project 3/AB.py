import copy

WHITE = 1
BLACK = -1
ROWS = 5
COLS = 5
### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Piece:

    def __init__(self, position, color):
        self.position = position
        if color == 'White':
            self.color = WHITE
        else:
            self.color = BLACK

    def get_chess_coord(self):
        return to_chess_coord(self.position)

    def get_type(self):
        return ""

    def get_reachable_position(self, board):
        pass

    def __str__(self):
        if self.color == WHITE:
            return self.get_type() + "-W"
        return self.get_type() + "-B"


class King(Piece):
    
    def get_reachable_position(self, board):
        r, c = self.position
        reachable = [
            (r-1, c-1), (r-1, c), (r-1, c+1),
            (r, c-1), (r, c+1),
            (r+1, c-1), (r+1, c), (r+1, c+1)
        ]
        res = list()
        for pos in reachable:
            pr, pc = pos
            if (pr >= 0) and (pr < ROWS) and (pc >= 0) and (pc < COLS) and ((board[pr][pc] is None) or board[pr][pc].color != self.color):
                res.append(pos)
        return res
    
    def get_type(self):
        return "King"


class Rook(Piece):

    def get_reachable_position(self, board):
        r, c = self.position
        res = list()
        pr, pc = r-1, c 
        while (pr >= 0) and (board[pr][pc] is None):
            res.append((pr, pc))
            pr -= 1
        if pr >= 0 and board[pr][pc].color != self.color:
            res.append((pr, pc))

        pr = r + 1
        while (pr < ROWS) and (board[pr][pc] is None):
            res.append((pr, pc))
            pr += 1
        if pr < ROWS and board[pr][pc].color != self.color:
            res.append((pr, pc))

        pr, pc = r, c-1
        while (pc >= 0) and (board[pr][pc] is None):
            res.append((pr, pc))
            pc -= 1 
        if pc >= 0 and board[pr][pc].color != self.color:
            res.append((pr, pc))

        pc = c + 1 
        while (pc < COLS) and (board[pr][pc] is None):
            res.append((pr, pc))
            pc += 1        
        if pc < COLS and board[pr][pc].color != self.color:
            res.append((pr, pc))
           
        return res

    def get_type(self):
        return "Rook"


class Bishop(Piece):

    def get_reachable_position(self, board):
        r, c = self.position
        res = list()
        pr, pc = r-1, c-1
        while (pr >= 0) and (pc >= 0) and (board[pr][pc] is None):
            res.append((pr, pc))
            pr -= 1
            pc -= 1
        if (pr >= 0) and (pc >= 0) and board[pr][pc].color != self.color:
            res.append((pr, pc))

        pr, pc = r-1, c+1
        while (pr >= 0) and (pc < COLS) and (board[pr][pc] is None):
            res.append((pr, pc))
            pr -= 1
            pc += 1
        if (pr >= 0) and (pc < COLS) and board[pr][pc].color != self.color:
            res.append((pr, pc))

        pr, pc = r+1, c-1
        while (pr < ROWS) and (pc >= 0) and (board[pr][pc] is None):
            res.append((pr, pc))
            pr += 1
            pc -= 1
        if (pr < ROWS) and (pc >= 0) and board[pr][pc].color != self.color:
            res.append((pr, pc))

        pr, pc = r+1, c+1
        while (pr < ROWS) and (pc < COLS) and (board[pr][pc] is None):
            res.append((pr, pc))
            pr += 1
            pc += 1
        if (pr < ROWS) and (pc < COLS) and board[pr][pc].color != self.color:
            res.append((pr, pc))

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
            (r+1, c-2), (r+1, c+2),           
            (r+2, c-1), (r+2, c+1)
        ]    
        for pos in reachable:
            pr, pc = pos
            if (pr >= 0) and (pr < ROWS) and (pc >= 0) and (pc < COLS) and ((board[pr][pc] is None) or board[pr][pc].color != self.color):
                res.append(pos)
        return res

    def get_type(self):
        return "Knight"


class Queen(Bishop, Rook):

    def get_reachable_position(self, board):
        return list(set(Rook.get_reachable_position(self, board) + Bishop.get_reachable_position(self, board)))

    def get_type(self):
        return "Queen"
        
class Pawn(Piece):
    def get_reachable_position(self, board):
        res = list()
        r, c = self.position
        if self.color == WHITE: # go downwards (r increases)
            if (r+1 < ROWS) and (board[r+1][c] is None):
                res.append((r+1, c))
            if (r+1 < ROWS) and (c-1 >= 0) and (board[r+1][c-1] is not None) and (board[r+1][c-1].color != self.color):
                res.append((r+1, c-1))
            if (r+1 < ROWS) and (c+1 < COLS) and (board[r+1][c+1] is not None) and (board[r+1][c+1].color != self.color):
                res.append((r+1, c+1))
        else: # go upwards (r decreases)
            if (r-1 >= 0) and (board[r-1][c] is None):
                res.append((r-1, c))
            if (r-1 >= 0) and (c-1 >= 0) and (board[r-1][c-1] is not None) and (board[r-1][c-1].color != self.color):
                res.append((r-1, c-1))
            if (r-1 >= 0) and (c+1 < COLS) and (board[r-1][c+1] is not None) and (board[r-1][c+1].color != self.color):
                res.append((r-1, c+1))
        return res

    def get_type(self):
        return "Pawn"


class State:
    
    def __init__(self, board, turn=WHITE):
        self.board = board
        self.turn = turn
    
    def actions(self):
        count_check = 0
        count_capture_queen = 0
        count_capture_rook = 0
        count_capture_knight_bishop = 0
        res = list()
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] is not None and self.board[r][c].color == self.turn:
                    for x in self.board[r][c].get_reachable_position(self.board):
                        if self.board[x[0]][x[1]] is not None and self.board[x[0]][x[1]].get_type() == "King":
                            res.insert(0, ((r, c), x))
                            count_check += 1
                        elif self.board[x[0]][x[1]] is not None and self.board[x[0]][x[1]].get_type() == "Queen":
                            res.insert(count_check, ((r, c), x))
                            count_capture_queen += 1
                        elif self.board[x[0]][x[1]] is not None and self.board[x[0]][x[1]].get_type() == "Rook":
                            res.insert(count_check + count_capture_queen, ((r, c), x))
                            count_capture_rook += 1
                        elif self.board[x[0]][x[1]] is not None and self.board[x[0]][x[1]].get_type() != "Pawn":
                            res.insert(count_check + count_capture_queen + count_capture_rook, ((r, c), x))
                            count_capture_knight_bishop += 1
                        elif self.board[x[0]][x[1]] is not None:
                            res.insert(count_check + count_capture_queen + count_capture_rook + count_capture_knight_bishop, ((r, c), x))
                        else:
                            res.append(((r, c), x))
        return res

    def result(self, action): # action is a tuple (old_position, new_position)
        board = [row[:] for row in self.board]
        res = State(board, -self.turn)
        res.board[action[0][0]][action[0][1]] = None
        piece = copy.deepcopy(self.board[action[0][0]][action[0][1]])
        piece.position = action[1]
        res.board[action[1][0]][action[1][1]] = piece
        return res
    
    def utility(self):
        max_util = 0
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] is not None:
                    if self.board[r][c].get_type() == "King":
                        max_util += 1000000 * self.board[r][c].color
                    elif self.board[r][c].get_type() == "Queen":
                        max_util += 90 * self.board[r][c].color
                    elif self.board[r][c].get_type() == "Rook":
                        max_util += 50 * self.board[r][c].color
                    elif self.board[r][c].get_type() == "Bishop":
                        max_util += 30 * self.board[r][c].color
                    elif self.board[r][c].get_type() == "Knight":
                        max_util += 30 * self.board[r][c].color
                    else:
                        max_util += 10 * self.board[r][c].color
        return max_util

    def is_terminal(self):
        count_kings = 0
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] is not None:
                    if self.board[r][c].get_type() == "King":
                        count_kings += 1
        return count_kings != 2
    
    def __str__(self):
        res = ""
        for row in self.board:
            for piece in row:
                if piece is None:
                    res += " --  "
                else:
                    res += str(piece) + " "
            res += "\n"
        return res

    def __hash__(self) -> int:
        res = str(self.turn) + str([[str(piece) for piece in row] for row in self.board])
        return hash(res)

action_record = dict()

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(state, depth, alpha, beta, is_max_player):
    global action_record

    if depth == 0 or state.is_terminal():
        return state.utility(), None
    move = None
    if is_max_player:
        value = -float('inf')
        if hash(state) not in action_record:
            action_record[hash(state)] = state.actions()
        actions = action_record[hash(state)]
        if len(actions) == 0:
            return 0, None
        for action in actions:
            v, _ = ab(state.result(action), depth-1, alpha, beta, False)
            if v > value:
                value, move = v, action
                alpha = max(alpha, value)
            if value >= beta:
                break
        return value, move
    else:
        value = float('inf')
        if hash(state) not in action_record:
            action_record[hash(state)] = state.actions()
        actions = action_record[hash(state)]
        if len(actions) == 0:
            return 0, None
        for action in actions:
            v, _ = ab(state.result(action), depth-1, alpha, beta, True)
            if v < value:
                value, move = v, action
                beta = min(beta, value)
            if value <= alpha:
                break
        return value, move


def from_chess_coord( ch_coord):
    return (int(ch_coord[1]), ord(ch_coord[0]) - 97)

def to_chess_coord(position):
    (r, c) = position
    return (chr(c+97), r)

def parse_gameboard(gameboard, pieces):
    for piece in gameboard:
        if gameboard[piece][0] == 'King':
            pieces.append(King(from_chess_coord(piece), gameboard[piece][1]))
        elif gameboard[piece][0] == 'Queen':
            pieces.append(Queen(from_chess_coord(piece), gameboard[piece][1]))
        elif gameboard[piece][0] == 'Knight':
            pieces.append(Knight(from_chess_coord(piece), gameboard[piece][1]))
        elif gameboard[piece][0] == 'Bishop':
            pieces.append(Bishop(from_chess_coord(piece), gameboard[piece][1]))
        elif gameboard[piece][0] == 'Rook':
            pieces.append(Rook(from_chess_coord(piece), gameboard[piece][1]))
        else:
            pieces.append(Pawn(from_chess_coord(piece), gameboard[piece][1]))

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type

    pieces = list()
    parse_gameboard(gameboard, pieces)

    board = [[None for _ in range(5)] for _ in range(5)]
    for piece in pieces:
        r, c = piece.position
        board[r][c] = piece

    state = State(board)
    _, move = ab(state, 4, -float('inf'), float('inf'), True)
    start, end = move

    return to_chess_coord(start), to_chess_coord(end)
