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

        while True:
            # show methods
            if not self.game.game_over:
                self.game.show_bg(screen)
                self.game.show_moves(screen)
                self.game.show_piece(screen)
                self.game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():
                    # click
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

                    # hold
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

                    # release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQ_SIZE
                            released_col = dragger.mouseX // SQ_SIZE

                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # check for valid move
                            if board.valid_move(dragger.piece, move):
                                board.pieces_that_can_eat = []
                                board.move(dragger.piece, move)
                                if dragger.piece.did_eat:
                                    self.game.move_cnt = 0
                            
                                # check for second move
                                if dragger.piece.has_second_eating_move:
                                    board.pieces_that_can_eat.append(dragger.piece)
                                    # set move cnt to 0 if piece has been eaten in game.py file
                                    self.game.next_turn()
                                self.game.next_turn()
                            
                                # Finish situations
                                self.game.finish()
                            
                            # show methods
                            self.game.show_bg(screen)
                            self.game.show_piece(screen)

                        

                        dragger.undrag_piece()

                    # exit
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                pygame.display.update()

            else: # Game over
                result_text = self.game.finish()

                # Display semi-transparent overlay
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(180)  # transparency
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))
                
                # Draw "Game Over" box
                font = pygame.font.Font(None, 50)
                result_surface = font.render(result_text, True, (0, 0, 0))
                result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

                # Button parameters
                button_font = pygame.font.Font(None, 36)
                play_again_surface = button_font.render("Play Again", True, (0, 0, 0))
                exit_surface = button_font.render("Exit", True, (0, 0, 0))

                play_again_rect = play_again_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
                exit_rect = exit_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))

                # Draw elements
                pygame.draw.rect(self.screen, (255, 255, 255), result_rect.inflate(20, 20))
                pygame.draw.rect(self.screen, (255, 255, 255), play_again_rect.inflate(20, 10))
                pygame.draw.rect(self.screen, (255, 255, 255), exit_rect.inflate(20, 10))
                
                self.screen.blit(result_surface, result_rect)
                self.screen.blit(play_again_surface, play_again_rect)
                self.screen.blit(exit_surface, exit_rect)

                pygame.display.update()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if play_again_rect.collidepoint(event.pos):
                                # Reset the game
                                self.game.reset()
                                board = self.game.board
                                dragger = self.game.dragger
                                self.mainloop()
                            elif exit_rect.collidepoint(event.pos):
                                pygame.quit()
                                sys.exit()

main = Main()
main.mainloop()