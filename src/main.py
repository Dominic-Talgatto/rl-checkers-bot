import pygame
import sys

from board import Board
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
            for event in pygame.event.get():
                self.game.show_bg(screen)
                self.game.show_piece(screen)
                self.game.show_moves(screen)
                self.game.show_hover(screen)
                
                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQ_SIZE
                    clicked_col = dragger.mouseX // SQ_SIZE

                    if self.game.board.squares[clicked_row][clicked_col].has_piece():
                        piece = self.game.board.squares[clicked_row][clicked_col].piece
                        if piece.color == self.game.next_player:
                            piece.clear_moves()
                            self.game.board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)

                            # show methods
                            self.game.show_bg(screen)
                            self.game.show_piece(screen)
                            self.game.show_moves(screen)
                            dragger.drag_piece(piece)
                
                
                #release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQ_SIZE
                        released_col = dragger.mouseX // SQ_SIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            board.move(piece, move)
                            if dragger.piece.has_second_eating_move:
                                self.game.next_turn()
                                dragger.piece.has_second_eating_move = False
                            self.game.next_turn()
                    self.game.show_bg(screen)
                    self.game.show_piece(screen)
                    self.game.show_hover(screen)

                            
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
                        self.game.show_piece(screen)
                        self.game.show_moves(screen)
                        self.game.show_hover(screen)
                        dragger.update_blit(screen)
            pygame.display.update()


main = Main()
main.mainloop()