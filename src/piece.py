import os

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None) -> None:
        self.name = name
        self.color = color
        value_sign = 1 if color == "white" else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.did_eat = False
        self.has_second_eating_move = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect



    def set_texture(self, size = 80):
        self.texture = os.path.join(f"assets/images/imgs-{size}px/{self.color}_{self.name}.png")
        
    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Checker(Piece):
    def __init__(self, color):
        if color == "white":
            self.dir = -1
        else:
            self.dir = 1
        super().__init__('pawn', color, 1.0)


class King(Piece):
    def __init__(self, color):
        if color == "white":
            self.dir = -1
        else:
            self.dir = 1
        super().__init__('king', color, 3.5)
