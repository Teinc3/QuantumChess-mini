import board
import piece

class Chess():
    """
    A class to represent the game of chess.
    
    ...

    Attributes:
    -----------
    board : Board
        represents the chess board of the game

    turn : bool
        True if white's turn

    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    promote(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece

    move(start:tup, to:tup) -> None
        Moves the piece at `start` to `to` if possible. Otherwise, does nothing.
    """

    def __init__(self):
        self.board = board.Board()

        self.turn = True

        self.white_ghost_piece = None
        self.black_ghost_piece = None

    def promotion(self, pos):
        pawn = None
        while pawn == None:
            promote = input("Promote pawn to [Q, R, N, B, P(or nothing)]: ")
            if promote not in ['Q', 'R', 'N', 'B', 'P', '']:
                print("Not a valid promotion piece")
            else:
                if promote == 'R':
                        pawn = piece.Rook(True)
        #         if promote == 'Q':
        #             pawn = piece.Queen(True)
        #         elif promote == 'R':
        #             pawn = piece.Rook(True)
        #         elif promote == 'N':
        #             pawn = piece.Knight(True)
        #         elif promote == 'B':
        #             pawn = piece.Bishop(True)
        #         elif promote == 'P' or promote == '':
        #             pawn = piece.Pawn(True)
        self.board.board[pos[0]][pos[1]] = pawn

    def move(self, start, to, qc, startq, toq):
        """
        Moves a piece at `start` to `to`. Does nothing if there is no piece at the starting point.
        Does nothing if the piece at `start` belongs to the wrong color for the current turn.
        Does nothing if moving the piece from `start` to `to` is not a valid move.

        start : tup
            Position of a piece to be moved

        to : tup 
            Position of where the piece is to be moved

        precondition: `start` and `to` are valid positions on the board
        """

        if self.board.board[start[0]][start[1]] == None:
            print("There is no piece to move at the start place")
            return

        target_piece = self.board.board[start[0]][start[1]]
        if self.turn != target_piece.color:
            print("That's not your piece to move")
            return

        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            print("There's a piece in the path.")
            return

        if target_piece.is_valid_move(self.board, start, to):
            # Special check for if the move is castling
            # Board reconfiguration is handled in Piece
            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:
                print("castled")

                if self.turn and self.black_ghost_piece:
                    self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
                elif not self.turn and self.white_ghost_piece:
                    self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None
                self.turn = not self.turn
                return

            if self.board.board[to[0]][to[1]]:
                print(str(self.board.board[to[0]][to[1]]) + " taken.")
                # Special logic for ghost piece, deletes the actual pawn that is not in the `to`
                # coordinate from en passant
                if self.board.board[to[0]][to[1]].name == "GP":
                    if self.turn:
                        self.board.board[
                            self.black_ghost_piece[0] + 1
                            ][
                            self.black_ghost_piece[1]
                        ] = None
                        self.black_ghost_piece = None
                    else:
                        self.board.board[self.white_ghost_piece[0] - 1][self.black_ghost_piece[1]] = None
                        self.white_ghost_piece = None

            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None
		qc.iswap(startq,toq)
            print(str(target_piece) + " moved.")

            if self.turn and self.black_ghost_piece:
                self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
            elif not self.turn and self.white_ghost_piece:
                self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None

            self.turn = not self.turn


def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """
    try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 5:
            print(s[0] + "is not in the range from 1 - 5")
            return None
        if col < 'a' or col > 'd':
            print(s[1] + "is not in the range from a - d")
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        return (row-1, dict[col])
    except:
        print(s + "is not in the format '[number][letter]'")
        return None

def quantum_translate(s):
	try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 5:
            print(s[0] + "is not in the range from 1 - 5")
            return None
        if col < 'a' or col > 'd':
            print(s[1] + "is not in the range from a - d")
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        return (5 * dict[col] + row - 1)
    except:
        print(s + "is not in the format '[number][letter]'")
        return None




if __name__ == "__main__":
    chess = Chess()
    chess.board.print_board()

    while True:
        start = input("From: ")
        to = input("To: ")

        qstart = quantum_translate(start)
        qto = quantum_translate(to)        
        start = translate(start)
        to = translate(to)




        if start == None or to == None:
            continue

        chess.move(start, to)
        quantum_jump(qstart, qto)

        chess.board.print_board()


 
def game_init():
	qur = QuantumRegister(20)
cr = ClassicalRegister(20)
qc = QuantumCircuit(qur,cr)
 
qc.x(qur[0])
qc.x(qur[6])
qc.x(qur[13])
qc.x(qur[19])
 
 
def quantum_jump(from, target):
	qc.iswap(from, target)
 
def split_jump(from, target_1, target_2):
	
 
def merge_jump(from_1, from_2, target):
	
 
def measure(pos):
	
	return 
 
‘’’
def out_of_bounds():
Already written in basis code
‘’’
