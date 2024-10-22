import pygame
import sys

from const import *
from game import Game
from move import Move
from square import Square

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

    def mainloop(self):
        dragger = self.game.dragger
        screen = self.screen
        board = self.game.board
        # game = self.game

        while True:

            # show methods
            self.game.show_bg(screen)
            self.game.show_moves(screen)
            self.game.show_piece(screen)
            self.game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQ_SIZE
                    clicked_col = dragger.mouseX // SQ_SIZE

                    if self.game.board.squares[clicked_row][clicked_col].has_piece():
                        piece = self.game.board.squares[clicked_row][clicked_col].piece
                        if piece.color == self.game.next_player:
                            # Check if piece is in board.pieces_that_can_eat or board.pieces_that_can_eat is empty
                            board.has_eating_pieces(piece.color)
                            if piece in board.pieces_that_can_eat or len(board.pieces_that_can_eat) == 0:
                                piece.clear_moves()
                                board.calc_moves(piece, clicked_row, clicked_col)
                                dragger.save_initial(event.pos)

                                # show methods
                                self.game.show_bg(screen)
                                self.game.show_moves(screen)
                                self.game.show_piece(screen)
                                dragger.drag_piece(piece)
                            else:
                                print("you have eating piece")
                        else:
                            print("choose another color")
                
                #release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:

                        board.pieces_that_can_eat = []

                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQ_SIZE
                        released_col = dragger.mouseX // SQ_SIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # check for valid move
                        if board.valid_move(dragger.piece, move):
                            board.move(piece, move)
                            # check for second move
                            if dragger.piece.has_second_eating_move:
                                self.game.next_turn()
                                dragger.piece.has_second_eating_move = False
                                board.pieces_that_can_eat.append(dragger.piece)
                            self.game.next_turn()
                        
                        # show methods
                        self.game.show_bg(screen)
                        self.game.show_piece(screen)
                        


                            
                    dragger.undrag_piece()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #hold
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[0] // SQ_SIZE
                    motion_col = event.pos[1] // SQ_SIZE
                    self.game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        self.game.show_bg(screen)
                        self.game.show_moves(screen)
                        self.game.show_piece(screen)
                        self.game.show_hover(screen)
                        dragger.update_blit(screen)


            
            pygame.display.update()

main = Main()
main.mainloop()