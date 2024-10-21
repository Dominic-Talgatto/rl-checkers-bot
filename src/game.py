import pygame

from const import *
from board import Board
from dragger import Dragger
from square import Square

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = "white"
        self.hovered_square = None

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_piece(self, surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = "#638046"
                center = (move.final.col * SQ_SIZE + SQ_SIZE // 2, move.final.row * SQ_SIZE + SQ_SIZE // 2)
                radius = SQ_SIZE // 8
                pygame.draw.circle(surface, color, center, radius)

    def show_hover(self, surface):
        if self.hovered_square:
            color = (180, 180, 180)
            rect = (self.hovered_square.row * SQ_SIZE, self.hovered_square.col * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hovered_square = self.board.squares[row][col] 