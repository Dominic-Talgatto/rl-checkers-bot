from copy import deepcopy
import pygame

# import board

def minimax(position, depth, max_player, game, alpha, beta):
    # if depth == 0 or position.winner() != None:
    #     return position.evaluate(), position
    if depth == 0:
        return position.evaluate(), position
    
    if position.next_player_board == "white":
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(deepcopy(position), 'white', game):
            evaluation = minimax(deepcopy(move), depth-1, False, game, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, maxEval)
            # if beta <= alpha:
                # break
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(deepcopy(position), 'black', game):
            evaluation = minimax(deepcopy(move), depth-1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            beta = min(alpha, minEval)
            # if beta <= alpha:
            #     break
        return minEval, best_move


def get_all_moves(board, color, game):
    boards = []
    
    if board.has_eating_pieces(color):
        for square in board.squares_that_can_eat:
            piece = deepcopy(square.piece)
            piece.clear_moves()
            board.calc_moves(piece, square.row, square.col)
            for move in piece.moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.squares[square.row][square.col].piece
                new_board = simulate_move(temp_piece, move, temp_board, game)
                boards.append(deepcopy(new_board))
                # print(move.final.row, move.final.col)
            # piece.clear_moves()
    else:
        for square in board.get_all_squares(color):
            piece = deepcopy(square.piece)
            piece.clear_moves()
            board.calc_moves(piece, square.row, square.col)
            for move in piece.moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.squares[square.row][square.col].piece
                new_board = simulate_move(temp_piece, move, temp_board, game)
                boards.append(deepcopy(new_board))
            # piece.clear_moves()

    return boards


def simulate_move(piece, move, board, game):
    board.move(piece, move)
    return deepcopy(board)

