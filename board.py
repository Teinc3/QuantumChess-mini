import piece

class Board():
    """
    A class to represent a chess board.

    ...

    Attributes:
    -----------
    board : list[list[Piece]]
        represents a chess board
        
    turn : bool
        True if white's turn

    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    print_board() -> None
        Prints the current configuration of the board

    move(start:tup, to:tup) -> None
        Moves the piece at `start` to `to` if possible. Otherwise, does nothing.
        
    """
    def __init__(self):
        """
        Initializes the board per standard chess rules
        """

        self.board = []

        # Board set-up
        for i in range(5):
            self.board.append([None] * 4)
        #note: I swapped the two
        # White
        self.board[4][3] = piece.Rook(False, False, None)
        self.board[3][2] = piece.King(False, False, None)


        # Black
        self.board[0][0] = piece.Rook(True, False, None)
        self.board[1][1] = piece.King(True, False, None)


    def print_board(self):
        """
        Prints the current state of the board.
        """

        buffer = ""
        for i in range(17):
            buffer += "*"
        print(buffer)
        t=0
        for i in range(len(self.board)):
            t += 1
            tmp_str=str(t)
            tmp_str += "|"
            for j in self.board[i]:
                if j == None or j.name == 'GP':
                    tmp_str += "   |"
                elif len(j.name) == 2:
                    tmp_str += (" " + str(j) + "|")
                else:
                    tmp_str += (" " + str(j) + " |")
            print(tmp_str)

        buffer = ""
        rows="   a   b   c   d  "
        print(rows)

        for i in range(17):
            buffer += "*"
        print(buffer)
