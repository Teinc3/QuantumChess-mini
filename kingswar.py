import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit.quantum_info.operators import Operator
import board
import piece
import copy
# import pyautogui
from qiskit import Aer, transpile

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
        # self.white_split = False
        # self.black_split = False

    def move(self, start, to, startq, toq, engine, sp, to2, toq2):
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
            print("There is no piece to move at the starting position.")
            return 0

        target_piece = self.board.board[start[0]][start[1]]
        if self.turn != target_piece.color:
            print("That's not your piece to move.")
            return 0
    
        if not sp: #normal move
            end_piece = self.board.board[to[0]][to[1]]
        else: #split move
            if target_piece.split == True:
                print("You cannot split a piece twice.")
                return 0
            if start == to:
                print(start)
                print(to)
                print("For a split move, the piece cannot stay in the original position.")
                return 0
            elif start == to2:
                print(start)
                print(to2)
                print("For a split move, the piece cannot stay in the original position.")
                return 0

        if target_piece.is_valid_move(self.board, start, to):
            if sp:
                if not target_piece.is_valid_move(self.board, start, to2):
                    return 0
                if self.board.board[to[0]][to[1]] != None or self.board.board[to2[0]][to2[1]] != None:
                    print("There is a piece in the split path.")
                    return 0
                if to == to2:
                    print("The endpoints of the split move cannot overlap.")
                    return 0
                    
            if self.board.board[to[0]][to[1]]:# there is something at the endpoint
                on_position = self.board.board[to[0]][to[1]]
                if on_position.color == target_piece.color: # same color piece at target
                    if on_position.name == target_piece.name and on_position.split and target_piece.split:# quantum merge at position
                        self.board.board[to[0]][to[1]] = target_piece
                        self.board.board[start[0]][start[1]] = None
                        self.board.board[to[0]][to[1]].split = False # full piece at position
                        self.turn = not self.turn #swap white and black
                        print("Your " + str(self.board.board[to[0]][to[1]]) + " merged at " + str(to))
                        return 0
                    else:# different piece, invalid
                        print("Your own piece already occupies the position.")
                        return 0
                else:# opposite color piece at target
                    if target_piece.split:# split piece capture
                        # if piece is split, we do local measurement first
                        print("Quantum measurement of " + str(self.board.board[start[0]][start[1]]) + " triggered.")
                        backend = Aer.get_backend('aer_simulator') # call simulator
                        circ.iswap(startq, anc[0])
                        circ.measure(anc[0], cr)
                        result = execute(circ, backend=backend, shots=1).result()
                        cbit_value = int(list(result.get_counts().keys())[0].split(' ')[0])
                        # print(cbit_value)
                        if cbit_value == 1:# the piece exists there
                            print("Your " + str(self.board.board[start[0]][start[1]]) + " is at " + str(start) + "!")# the other piece collapsed
                            # print(str(self.board.board[to[0]][to[1]]) + " taken.)
                            target_piece.split = False
                            self.board.board[target_piece.joint[0]][target_piece.joint[1]] = None
                            target_piece.joint = None
                            if on_position.split: # self measure exists, opponent split
                                print("Quantum measurement of " + str(self.board.board[to[0]][to[1]]) + " at " + str(to) + " triggered.")
                                backend = Aer.get_backend('aer_simulator') # call simulator
                                circ.iswap(toq, anc[0]) # note toq
                                circ.measure(anc[0], cr)
                                result = execute(circ, backend=backend, shots=1).result()
                                cbit_value = int(list(result.get_counts().keys())[0].split(' ')[0])
                                if cbit_value == 1: # the piece to be captured also exists
                                    print("Their " + str(self.board.board[to[0]][to[1]]) + " is at " + str(to) + "!")
                                    on_position.split = False
                                    self.board.board[on_position.joint[0]][on_position.joint[1]] = None
                                    on_position.joint = None
                                    print("Opponent " + str(self.board.board[to[0]][to[1]]) + " at " + str(to) + " captured.")# start capture
                                    self.board.board[to[0]][to[1]] = target_piece # classic capture
                                    self.board.board[start[0]][start[1]] = None
                                    self.turn = not self.turn #swap white and black
                                    if on_position.name == "K":
                                        if on_position.color:# white king captured
                                            print("Congratulations! Black wins!")
                                        else:
                                            print("Congratulations! White wins!")
                                        #pyautogui.hotkey('ctrl', 'm', 'i')# stop
                                    return 1
                                else: # the piece to be captured does not exist
                                    print("Their " + str(self.board.board[to[0]][to[1]]) + " is at " + str(on_position.joint) + "!")
                                    # here we change the split piece back into non-split
                                    self.board.board[on_position.joint[0]][on_position.joint[1]].split = False
                                    self.board.board[on_position.joint[0]][on_position.joint[1]].joint = None
                                    print("Your " + str(self.board.board[start[0]][start[1]]) + " has captured nothing?!")
                                    self.board.board[to[0]][to[1]] = target_piece #simple move
                                    self.board.board[start[0]][start[1]] = None
                                    self.turn = not self.turn #swap white and black
                                    return 0
                            else: # self measure exists, opponent non-split
                                print("Opponent " + str(self.board.board[to[0]][to[1]]) + " at " + str(to) + " captured.")# start capture
                                self.board.board[to[0]][to[1]] = target_piece # classic capture
                                self.board.board[start[0]][start[1]] = None
                                self.turn = not self.turn #swap white and black
                                if on_position.name == "K":
                                    if on_position.color:# white king captured
                                        print("Congratulations! Black wins!")
                                    else:
                                        print("Congratulations! White wins!")
                                    # pyautogui.hotkey('ctrl', 'm', 'i') # stop
                                return 1
                        else: # our piece doesn't exist there in order for the capture to happen
                            print("The real " + str(self.board.board[start[0]][start[1]]) + " is at " + str(target_piece.joint) + "!")
                            self.board.board[target_piece.joint[0]][target_piece.joint[1]].split = False
                            self.board.board[target_piece.joint[0]][target_piece.joint[1]].joint = None
                            self.board.board[start[0]][start[1]] = None
                            print("Capture sequence cancelled. Switching turns...")
                            self.turn = not self.turn #swap white and black
                            return 0
                    else: # our piece isn't split
                        if on_position.split: # opponent split
                            print("Quantum measurement of " + str(self.board.board[to[0]][to[1]]) + " at " + str(to) + " triggered.")
                            backend = Aer.get_backend('aer_simulator') # call simulator
                            circ.iswap(toq, anc[0]) # note toq
                            circ.measure(anc[0], cr)
                            result = execute(circ, backend=backend, shots=1).result()
                            cbit_value = int(list(result.get_counts().keys())[0].split(' ')[0])
                            if cbit_value == 1: # the piece to be captured exists
                                print("The real " + str(self.board.board[to[0]][to[1]]) + " is at " + str(to) + "!")
                                on_position.split = False
                                self.board.board[on_position.joint[0]][on_position.joint[1]] = None
#                                print(on_position.joint[0])
#                                print(on_position.joint[1])
                                on_position.joint = None
                                print("Opponent " + str(self.board.board[to[0]][to[1]]) + " at " + str(to) + " captured.")# start capture
                                self.board.board[to[0]][to[1]] = target_piece # classic capture
                                self.board.board[start[0]][start[1]] = None
                                self.turn = not self.turn #swap white and black
                                if on_position.name == "K":
                                    if on_position.color:# white king captured
                                        print("Congratulations! Black wins!")
                                    else:
                                        print("Congratulations! White wins!")
                                    #pyautogui.hotkey('ctrl', 'm', 'i')# stop in google colab environment
                                return 1
                            else: # the piece to be captured does not exist
                                print("The real " + str(self.board.board[to[0]][to[1]]) + " is at " + str(on_position.joint) + "!")
                                # here we change the split piece back into non-split
                                self.board.board[on_position.joint[0]][on_position.joint[1]].split = False
                                self.board.board[on_position.joint[0]][on_position.joint[1]].joint = None
                                print("Your " + str(self.board.board[start[0]][start[1]]) + " has captured nothing?!")
                                self.board.board[to[0]][to[1]] = target_piece #simple move
                                self.board.board[start[0]][start[1]] = None
                                self.turn = not self.turn #swap white and black
                                return 0
                        else: # self measure exists, opponent non-split
                            print("Opponent " + str(self.board.board[to[0]][to[1]]) + " at " + str(to) + " captured.")# start capture
                            self.board.board[to[0]][to[1]] = target_piece # classic capture
                            self.board.board[start[0]][start[1]] = None
                            self.turn = not self.turn #swap white and black
                            if on_position.name == "K":
                                if on_position.color:# white king captured
                                    print("Congratulations! Black wins!")
                                else:
                                    print("Congratulations! White wins!")
#                                pyautogui.hotkey('ctrl', 'm', 'i')# stop
                            return 1
            else:# classic move, nothing at end
                if sp:#if split why is this frickin iswap
                    sqrt2 = np.sqrt(2)
                    Matrix = Operator([
                        [1, 0, 0, 0],
                        [0, 1 / sqrt2, 1j / sqrt2, 0],
                        [0, 1j / sqrt2, 1 / sqrt2, 0],
                        [0, 0, 0, 1]])
                    circ.unitary(Matrix, [startq, toq])# oh in unitary those both are the same cuz startq and toq
                    circ.iswap(startq,toq2)
                    target_piece.split = True
                    new_piece = copy.deepcopy(target_piece) # just figured out that in python = points to the same memory so the edit in joint property changes in both squares and caused quite some problems
                    self.board.board[to[0]][to[1]] = target_piece # don't know what this part is for but ok
                    self.board.board[to[0]][to[1]].joint = (to2[0],to2[1])
                    self.board.board[to2[0]][to2[1]] = new_piece
                    self.board.board[to2[0]][to2[1]].joint = (to[0],to[1])
                    print(str(target_piece) + " splittt.")
                else:# moved piece
                    circ.iswap(startq,toq)
                    print(str(target_piece) + " moved.")
                    self.board.board[to[0]][to[1]] = target_piece
                    if target_piece.split: #moved split piece, update friend
                        self.board.board[target_piece.joint[0]][target_piece.joint[1]].joint = (to[0],to[1])
                self.board.board[start[0]][start[1]] = None
                self.turn = not self.turn #swap white and black
                return 0

def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """
    try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 5:
            print(s[0] + " is not in the range from 1 - 5")
            return None
        if col < 'a' or col > 'd':
            print(s[1] + " is not in the range from a - d")
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        return (row-1, dict[col])
    except:
        print(s + " is not in the format '[number][letter]'")
        return None

def transq(s):
    if s == None:
        print("Please input in the correct format '[number][letter]'.")
        return
    a = np.arange(0, 20).reshape(5,4)
    qn=a[s[0]][s[1]]
    return int(qn)

def checklen(s):
    if len(s)==4:
        return True
    else:
        return False

def game_ended():
    return end
    #note: no more pieces in the state of king
#note: problem is white split a piece but black has the same variable recording if they split so needa fix later on
if __name__ == "__main__":
    chess = Chess()
    chess.board.print_board()
    qr = QuantumRegister(20, 'q')
    anc = QuantumRegister(1, 'ancilla')
    cr = ClassicalRegister(1, 'c')
    circ = QuantumCircuit(qr,anc,cr)

    circ.x(0)
    circ.x(5)
    circ.x(14)
    circ.x(19)
    to2 = 0
    toq2 = 0
    cont = 1
    while cont == 1:
        split = False
        start = input("From: ")
        to = input("To: ")
        start = translate(start)
        if checklen(to):# if the length is 4, split move
            to1 = translate(to[:2])
            to2 = translate(to[2:4])
            startq = transq(start)
            toq1 = transq(to1)
            toq2 = transq(to2)
            #print(toq1)
            #print(toq2)
            if start == None or to == None or to1 == None or to2 == None:
                continue
            split = True
            if chess.move(start, to1, startq, toq1, circ, split, to2, toq2):
                cont = 0
            to2 = 0
        else:
            to = translate(to)
            startq = transq(start)
            toq = transq(to)
            if start == None or to == None:
                continue
            if chess.move(start, to, startq, toq, circ, split, to2, toq2):
                cont = 0
        #print(circ) #uh we remove printing the whole frickin circuit everytime
        chess.board.print_board()
