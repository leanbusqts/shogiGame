"""
*Positions are done row-column.
*Alpha-Number system.
*Specified as tuples.
"""

SENTE = "SENTE"  # Letras MAYUSCULAS, es quien comienza el juego.
GOTE = "GOTE"  # Letras minusculas.

"""Pieces
King K: "♔", Gold G: "♕", Silver S: "♕", Knight N: "♘", Lance L: "♗", Bishop B: "♗", Rook R: "♖", Pawn P: "♙"
{GOTE: {K: "♔", G: "♕", S: "♕", N: "♘", L: "♗", B: "♗", R: "♖", P: "♙"},
SENTE: {K: "♚", G: "♛", S: "♛", N: "♞", L: "♝", B: "♝", R: "♜", P: "♟"}}
"Uni" = unicode characters
"""


class Game:
    def __init__(self):
        self.playersTurn = SENTE
        self.board = {}
        self.placePieces()
        print("Algebraic notation separated by space")
        print("Sente pieces in 'UPPER' case and Gote pieces in 'lower' case")
        self.main()

    def placePieces(self):
        # Pawns
        for i in range(0, 9):
            self.board[(i, 2)] = P(GOTE, uniPieces[GOTE][P], 1)
            self.board[(i, 6)] = P(SENTE, uniPieces[SENTE][P], -1)
        # Bishop
        self.board[(1, 1)] = B(GOTE, uniPieces[GOTE][B], 1)
        self.board[(7, 7)] = B(SENTE, uniPieces[SENTE][B], -1)
        # Rook
        self.board[(7, 1)] = R(GOTE, uniPieces[GOTE][R], 1)
        self.board[(1, 7)] = R(SENTE, uniPieces[SENTE][R], -1)
        # BackLine
        placers = [L, N, S, G, K, G, S, N, L]
        for i in range(0, 9):
            self.board[(i, 0)] = placers[i](GOTE, uniPieces[GOTE][placers[i]], 1)
            self.board[(i, 8)] = placers[i](SENTE, uniPieces[SENTE][placers[i]], -1)

    def main(self):

        while True:
            self.printBoard()
            startPos, endPos = self.usrInput()
            self.playersTurn
            try:
                target = self.board[startPos]
            except KeyError:
                print("out of range")
                target = None

            if target:
                if target.color != self.playersTurn:
                    print("It's not your turn")
                    continue
                if target.isValid(startPos, endPos, target.color, self.board):
                    # auto check
                    # update position
                    self.board[endPos] = self.board[startPos]
                    del self.board[startPos]
                    # is check
                    self.isCheck()
                    # change turn
                    self.changeTurn()
                else:
                    print("invalid move")
            # else:
            #    print("try again")

    def isCheck(self):
        uniKing = {}
        pieceUni = {SENTE: [], GOTE: []}
        for position, piece in self.board.items():
            if type(piece) == K:
                uniKing[piece.color] = position
            pieceUni[piece.color].append((piece, position))
        # print(pieceUni)
        # white
        if self.seeKing(uniKing[GOTE], pieceUni[SENTE]):
            print("Gote player is in check")
        if self.seeKing(uniKing[SENTE], pieceUni[GOTE]):
            print("Sente player is in check")

    def seeKing(self, kingPos, pieceList):
        for piece, position in pieceList:
            if piece.isValid(position, kingPos, piece.color, self.board):
                return True

    def printBoard(self):
        print("    1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |")
        print("-"*39)
        for i in range(0, 9):
            print(chr(i+97), end=" | ")
            for j in range(0, 9):
                item = self.board.get((i, j), " ")
                print(str(item)+' |', end=" ")
            print()

    def usrInput(self):  # Input from user
        try:
            a, b = input().split()
            a = ((ord(a[0])-97), int(a[1])-1)
            b = (ord(b[0])-97, int(b[1])-1)
            return (a, b)
        except ValueError:
            print("error decoding input.")
            return((-1, -1), (-1, -1))
        except IndexError:
            print("invalid input, try again")
            return((-1, -1), (-1, -1))

    def changeTurn(self):
        if self.playersTurn == SENTE:
            self.playersTurn = GOTE
        else:
            self.playersTurn = SENTE


class Piece:

    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.position = None

    def isValid(self, startPos, endPos, color, board):
        # if endPos (in self.isMove(startPos[0], startPos[1], board, color=Color) and isAutoCheck():
        # Chequea que endPos sea un movimiento permitido por la pieza
        if endPos in self.isMove(startPos[0], startPos[1], board, color=color):
            return True
        return False

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def isMove(self, y, x, board):
        print("ERROR movement")

    def lineMove(self, y, x, board, color, intervals):
        movement = []
        for yint, xint in intervals:
            ytemp, xtemp = y+yint, x+xint
            while self.isInBoard(ytemp, xtemp):
                target = board.get((ytemp, xtemp), None)
                if target is None:
                    movement.append((ytemp, xtemp))
                elif target.color != color:
                    movement.append((ytemp, xtemp))
                    break
                else:
                    break
                ytemp, xtemp = ytemp + yint, xtemp + xint
        return movement

    def isInBoard(self, y, x):  # Position on the board
        if y >= 0 and y < 9 and x >= 0 and x < 9:
            return True
        return False

    def noConflict(self, board, initialColor, y, x):  # Checks position poses no conflict to the rules
        if self.isInBoard(y, x) and (((y, x) not in board) or board[(y, x)].color != initialColor):
            return True
        return False


lineCardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
lineDiagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


class K(Piece):  # King
    def __init__(self, color, name, direction):
        self.color = color
        self.name = name
        self.direction = direction

    def kingMoves(self, y, x):
        return [(y, x-1), (y-1, x-1), (y-1, x), (y-1, x+1), (y, x+1), (y+1, x+1), (y+1, x), (y+1, x-1)]

    def isMove(self, y, x, board, color=None):
        if color is None:
            color = self.color
        return [(yy, xx) for yy, xx in self.kingMoves(y, x) if self.noConflict(board, color, yy, xx)]


class G(Piece):  # Gold
    def __init__(self, color, name, direction):
        self.color = color
        self.name = name
        self.direction = direction

    def goldMoves(self, y, x):
        return [(y, x+self.direction), (y-1, x+self.direction), (y-1, x), (y, x-self.direction), (y+1, x), (y+1, x+self.direction)]

    def isMove(self, y, x, board, color=None):
        if color is None:
            color = self.color
        return [(yy, xx) for yy, xx in self.goldMoves(y, x) if self.noConflict(board, color, yy, xx)]


class S(Piece):  # Silver
    def __init__(self, color, name, direction):
        self.color = color
        self.name = name
        self.direction = direction

    def silverMoves(self, y, x):
        return [(y, x+self.direction), (y-1, x+self.direction), (y-1, x-self.direction), (y+1, x-self.direction), (y+1, x+self.direction)]

    def isMove(self, y, x, board, color=None):
        if color is None:
            color = self.color
        return [(yy, xx) for yy, xx in self.silverMoves(y, x) if self.noConflict(board, color, yy, xx)]


class N(Piece):  # Knight
    def __init__(self, color, name, direction):
        self.color = color
        self.name = name
        self.direction = direction

    def knightMoves(self, y, x):
        return [(y+1, x+self.direction+self.direction), (y-1, x+self.direction+self.direction)]

    def isMove(self, x, y, board, color=None):
        if color is None:
            color = self.color
        return [(xx, yy) for xx, yy in self.knightMoves(x, y) if self.noConflict(board, color, xx, yy)]


class L(Piece):  # Lance
    def __init__(self, color, name, direction):
        self.color = color
        self.name = name
        self.direction = direction
        self.lineLance = [(0, self.direction)]

    def isMove(self, y, x, board, color=None):
        if color is None:
            color = self.color
        return self.lineMove(y, x, board, color, self.lineLance)


class R(Piece):  # Rook
    def __init__(self, color, name, direction):
        self.color = color
        self.name = name
        self.direction = direction
        self.lineRook = lineCardinals

    def isMove(self, y, x, board, color=None):
        if color is None:
            color = self.color
        return self.lineMove(y, x, board, color, self.lineRook)


class B(Piece):  # Bishop
    def __init__(self, color, name, direction):
        self.color = color
        self.name = name
        self.direction = direction
        self.lineBishop = lineDiagonals

    def isMove(self, y, x, board, color=None):
        if color is None:
            color = self.color
        return self.lineMove(y, x, board, color, self.lineBishop)


class P(Piece):  # Pawn
    def __init__(self, color, name, direction):
        self.color = color
        self.name = name
        self.direction = direction

    def pawnMoves(self, y, x):
        return [(y, x+self.direction)]

    def isMove(self, y, x, board, color=None):
        if color is None:
            color = self.color
        return [(yy, xx) for yy, xx in self.pawnMoves(y, x) if self.noConflict(board, color, yy, xx)]


uniPieces = {GOTE: {K: "k", G: "g", S: "s", N: "n", L: "l", B: "b", R: "r", P: "p"}, SENTE: {K: "K", G: "G", S: "S", N: "N", L: "L", B: "B", R: "R", P: "P"}}


Game()
