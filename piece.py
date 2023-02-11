blocked_path = "There's a piece in the path."
incorrect_path = "This piece does not move in this pattern."
blockq = "There's a quantum piece in the path."

def check_updown(board, start, to):
    """
    Checks if there are no pieces along the vertical or horizontal path
    from `start` (non-inclusive) to `to` (non-inclusive).

    board : Board
        Representation of the current board

    start : tup
        Start location of diagonal path

    to : tup
        End location of diagonal path
    """
    if start[0] == to[0]:
        smaller_y = start[1] if start[1] < to[1] else to[1]
        bigger_y = start[1] if start[1] > to[1] else to[1]

        for i in range(smaller_y + 1, bigger_y):
            if board.board[start[0]][i] != None:
                q = start[0] + 1
                k = chr(i + ord('a'))
                print("At: " + str(q)+ str(k))
                print(blocked_path)
                return False
        return True
    else:
        smaller_x = start[0] if start[0] < to[0] else to[0]
        bigger_x = start[0] if start[0] > to[0] else to[0]

        for i in range(smaller_x + 1, bigger_x):
            if board.board[i][start[1]] != None:
                q = i + 1
                k = chr(start[1] + ord('a'))
                print("At: " + str(q) + str(k))
                print(blocked_path)
                return False
        return True



class Piece():
    """
    A class to represent a piece in chess
    
    ...

    Attributes:
    -----------
    name : str
        Represents the name of a piece as following - 
        Pawn -> P
        Rook -> R
        Knight -> N
        Bishop -> B
        Queen -> Q
        King -> K

    color : bool
        True if piece is white
        
    split : bool
        True if piece is split
    
    joint : tup
      storing coordinates of other split piece to update entangled pieces
        
    Methods:
    --------
    is_valid_move(board, start, to) -> bool
        Returns True if moving the piece at `start` to `to` is a legal
        move on board `board`
        Precondition: [start] and [to] are valid coordinates on the board.board
        
    is_white() -> bool
        Return True if piece is white
        
    is_split() -> bool
        Return True if piece is split
    """
    def __init__(self, color, split, joint):
        self.name = ""
        self.color = color
        self.split = False
        self.joint = None

    def is_valid_move(self, board, start, to):
        return False

    def is_white(self):
        return self.color
    
    def is_split(self):
        return self.split
        
    def __str__(self):
        if self.color:#white
            return '\033[94m' + self.name + '\033[0m'
        else:
            return self.name

class Rook(Piece):
    def __init__(self, color, split, joint, first_move = True):
        """
        Same as base class Piece, except `first_move` is used to check
        if this rook can castle.
        """
        super().__init__(color, split, joint)
        self.name = "R"
        self.first_move = first_move 

    def is_valid_move(self, board, start, to):
        if start[0] == to[0] or start[1] == to[1]:
            return check_updown(board, start, to)
        print(incorrect_path)
        return False

class King(Piece):
    def __init__(self, color, split, joint, first_move = True):
        """
        Same as base class Piece, except `first_move` is used to check
        if this king can castle.
        """
        super().__init__(color, split, joint)
        self.name = "K"
        self.first_move = first_move

    def is_valid_move(self, board, start, to):
        if self.first_move and abs(start[1] - to[1]) == 2 and start[0] - to[0] == 0:
            return self.can_castle(board, start, to, to[1] - start[1] > 0)

        if abs(start[0] - to[0]) == 1 or start[0] - to[0] == 0:
            if start[1] - to[1] == 0 or abs(start[1] - to[1]) == 1:
                self.first_move = False
                return True

        print(incorrect_path)
        return False
