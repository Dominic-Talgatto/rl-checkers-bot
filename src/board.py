from const import *
from square import Square
from piece import Checker
from piece import King
from move import Move


class Board:
    def __init__(self):
        self.squares = []
        self._create_board()
        self._add_pieces("white")
        self._add_pieces("black")
        self.pieces_that_can_eat = []

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        piece.has_second_eating_move = False
        piece.did_eat = False

        # for pawns
        if piece.name == "pawn":
            # check if pawn eat another piece
            if abs(initial.row - final.row) == 2:
                difference_row = (final.row - initial.row) // 2
                difference_col = (final.col - initial.col) // 2
                eaten_piece_row = initial.row + difference_row
                eaten_piece_col = initial.col + difference_col

                self.squares[eaten_piece_row][eaten_piece_col].piece = None
                piece.did_eat = True
                possible_moves = [
                    (final.row + 1, final.col - 1),
                    (final.row + 1, final.col + 1),
                    (final.row - 1, final.col - 1),
                    (final.row - 1, final.col + 1)
                ]
                piece.has_second_eating_move = self.pawns_eating_moves(piece, final.row, final.col, possible_moves)

            self.squares[initial.row][initial.col].piece = None
            self.squares[final.row][final.col].piece = piece
        else: # for kings
            dir_r = (final.row - initial.row) // abs(final.row - initial.row)
            dir_c = (final.col - initial.col) // abs(final.col - initial.col)
            temp_r, temp_c = initial.row, initial.col 
            while True:
                temp_r += dir_r
                temp_c += dir_c  

                if Square.in_range(temp_r, temp_c):
                    if self.squares[temp_r][temp_c].has_rival_piece(piece.color):
                        self.squares[temp_r][temp_c].piece = None
                        piece.did_eat = True
                        
                        while True:
                            temp_r += dir_r
                            temp_c += dir_c
                            
                            if Square.in_range(temp_r, temp_c) and self.squares[temp_r][temp_c].isempty():
                                dirs = [
                                    [-1, -1],
                                    [-1, 1],
                                    [1, -1],
                                    [1, 1]
                                ]
                                dirs.remove([-1 * dir_r, -1 * dir_c])
                                for d in dirs:
                                    if self.king_has_second_eating_move(piece, temp_r, temp_c, d):
                                        piece.has_second_eating_move = True
                            else:
                                break
                            if abs(temp_r) == abs(final.row) and abs(temp_c) == abs(final.col):
                                break
                else:       
                  break

                if abs(temp_r) == abs(final.row) and abs(temp_c) == abs(final.col):
                    break

            self.squares[initial.row][initial.col].piece = None
            self.squares[final.row][final.col].piece = piece


        # Check if pawn can be turn into kings 
        if piece.name == "pawn":
            r = 0 if piece.color == "white" else 7
            if final.row == r:
                # piece.name = "king"
                color = piece.color
                self.squares[final.row][final.col] = None
                self.squares[final.row][final.col] = Square(final.row, final.col, Checker(color))


        piece.moved = True

        # clear valid moves
        piece.clear_moves()

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):
        def pawn_moves():
            # for eating
            possible_moves = [
                (row + 1, col - 1),
                (row + 1, col + 1),
                (row - 1, col - 1),
                (row - 1, col + 1)
            ]

            self.pawns_eating_moves(piece, row, col, possible_moves)

            # If piece don't have eating piece
            if len(piece.moves) == 0:
                # for moving
                if piece.dir == 1: 
                    possible_moves = [
                        (row + 1, col - 1),
                        (row + 1, col + 1)
                    ]
                else:
                    possible_moves = [
                        (row - 1, col - 1),
                        (row - 1, col + 1)
                    ]

                
                for possible_move in possible_moves:
                    possible_move_row, possible_move_col = possible_move
                    if Square.in_range(possible_move_row, possible_move_col):
                        if self.squares[possible_move_row][possible_move_col].isempty(): ###
                            # creating new move squares
                            initial = Square(row, col)
                            final = Square(possible_move_row, possible_move_col)
                            # creating new move
                            move = Move(initial, final)
                            piece.add_move(move)


        def king_moves():
            # # for eating
            dirs = [
                [-1, -1],
                [-1, 1],
                [1, -1],
                [1, 1]
            ]

            for dir in dirs:
                self.kings_eating_moves(piece, row, col, dir)

            # for moving
            if len(piece.moves) == 0:
                dirs = [
                    [-1, -1],
                    [-1, 1],
                    [1, -1],
                    [1, 1]
                ]

                for dir in dirs:
                    self.kings_moves(piece, row, col, dir)


        if piece.name == 'pawn':
            pawn_moves()

        elif piece.name == 'king':
            king_moves()

    # returns if it has eating move
    def pawns_eating_moves(self, piece, row, col, dir):
        has_eating_move = False

        for possible_move in dir:
            possible_rival_piece_row, possible_rival_piece_col = possible_move
            # getting row and col after rival piece
            difference_of_row = ((row - possible_rival_piece_row) * 2)
            difference_of_col = ((col - possible_rival_piece_col) * 2)
            possible_move_row, possible_move_col = row - difference_of_row, col - difference_of_col
            if Square.in_range(possible_move_row, possible_move_col) and Square.in_range(possible_rival_piece_row, possible_rival_piece_col) :
                if self.squares[possible_move_row][possible_move_col].isempty() and self.squares[possible_rival_piece_row][possible_rival_piece_col].has_rival_piece(piece.color): ###
                    # creating new move squares
                    initial = Square(row, col)
                    final = Square(possible_move_row, possible_move_col)
                    # creating new move
                    move = Move(initial, final)
                    piece.add_move(move)
                    has_eating_move = True

        
        return has_eating_move

    # returns if it has eating move
    def kings_eating_moves(self, piece, row, col, dir):
        dir_r = dir[0]
        dir_c = dir[1]
        init_r = row
        init_c = col
        has_eating_move = False
        bool_ = False

        while True:
            row += dir_r
            col += dir_c
            if Square.in_range(row, col):
                if self.squares[row][col].has_team_piece(piece.color):
                    break
                elif self.squares[row][col].has_rival_piece(piece.color):
                    while True:
                        row += dir_r
                        col += dir_c
                        if Square.in_range(row, col) and self.squares[row][col].isempty():
                            dirs = [
                                [-1, -1],
                                [-1, 1],
                                [1, -1],
                                [1, 1]
                            ]
                            dirs.remove([-1 * dir_r, -1 * dir_c])
                            if not bool_:
                                initial = Square(init_r, init_c)
                                final = Square(row, col)
                                # creating new move
                                move = Move(initial, final)
                                piece.add_move(move)
                                has_eating_move = True

                                for d in dirs:
                                    if self.king_has_second_eating_move(piece, row, col, d):
                                        piece.clear_moves()
                                        bool_ = True
                                        initial = Square(init_r, init_c)
                                        final = Square(row, col)
                                        # creating new move
                                        move = Move(initial, final)
                                        piece.add_move(move)
                                        # piece.has_second_eating_move = True
                            else:
                                for d in dirs:
                                    if self.king_has_second_eating_move(piece, row, col, d):
                                        initial = Square(init_r, init_c)
                                        final = Square(row, col)
                                        # creating new move
                                        move = Move(initial, final)
                                        piece.add_move(move)

                                
                        else: 
                            break
                else: # if square is empty
                    continue
            if init_r <= abs(row) and init_c <= abs(col):
                break
        return has_eating_move

    def kings_moves(self, piece, row, col, dir):
        init_r = row
        init_c = col
        dir_r = dir[0]
        dir_c = dir[1]

        while True:
            row += dir_r
            col += dir_c
            if Square.in_range(row, col):
                if self.squares[row][col].isempty():
                    initial = Square(init_r, init_c)
                    final = Square(row, col)
                    # creating new move
                    move = Move(initial, final)
                    piece.add_move(move)
                else: break
            else: break
   
    def king_has_second_eating_move(self, piece, row, col, dir):
            dir_r = dir[0]
            dir_c = dir[1]
            hsem = False # has_second_eating_move

            while True:
                row += dir_r
                col += dir_c
                if Square.in_range(row, col):
                    if self.squares[row][col].has_team_piece(piece.color):
                        break
                    elif self.squares[row][col].has_rival_piece(piece.color):
                        while True:
                            row += dir_r
                            col += dir_c
                            if Square.in_range(row, col) and self.squares[row][col].isempty():
                                hsem = True
                            else: 
                                break
                    else: # if square is empty
                        continue
                else:
                    break
            return hsem
   
    def has_eating_pieces(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.squares[i][j].piece
                can_eat = False
                row = i
                col = j
                if piece and piece.color == color:
                    if piece.name == "pawn":
                        possible_moves = [
                            (row + 1, col - 1),
                            (row + 1, col + 1),
                            (row - 1, col - 1),
                            (row - 1, col + 1)
                        ]
                        can_eat = self.pawns_eating_moves(piece, row, col, possible_moves)
                    else:
                        dirs = [
                            [-1, -1],
                            [-1, 1],
                            [1, -1],
                            [1, 1]
                        ]
                        for d in dirs:
                            if not can_eat:
                                can_eat = self.king_has_second_eating_move(piece, row, col, d)
                    
                    if can_eat:
                        self.pieces_that_can_eat.append(piece)

    def _create_board(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLUMNS)]

        for row in range(ROWS):
            for col in range(COLUMNS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        if color == "black":
            row_checkers = [0, 1, 2]
        else:
            row_checkers = [5, 6, 7]

        
        for row in row_checkers:
            for col in range(COLUMNS):
                if (row + col) % 2 == 1:
                    self.squares[row][col] = Square(row, col, Checker(color))
            # self.squares[3][2] = Square(3, 2, Checker("white"))
            # self.squares[4][3] = Square(4, 3, King("black"))