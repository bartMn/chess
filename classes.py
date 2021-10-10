import pygame
import os
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)

BOARD_WIDTH= 700

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)

class Coordinates(pygame.sprite.Sprite):
     def __init__(self, location, ID, char, color):
        super(Coordinates, self).__init__()
        self.text = font.render(char, True, (0, 0, 0), color)
        self.location = location
        self.ID = ID


class Square(pygame.sprite.Sprite):
    def __init__(self, color, size, position_x, position_y, ID, occupied_by = None):
        super(Square, self).__init__()

        self.position_x= position_x
        self.position_y= position_y
        self.size= size
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect(
            center=(
                self.position_x + size/2,
                self.position_y + size/2,
            )
        )
        self.ID = ID
        black, dif_col = color
        if black == True:
            self.color= (153, 76, 0)
        elif black == False:
            self.color= (255, 255, 255)
        else:
            self.color = dif_col
        
        #print(color)
        self.surf.fill(self.color)
        self.is_pressed = False
        self.occupied_by = occupied_by

    def change_color(self, Squares_cliced, col = None):
        if not self.is_pressed:
            #self.surf.fill(self.color)
            #self.surf.fill((0,0,255))
            self.new_square= Square((None, col), self.size, 0, 0, self.ID)
            self.surf.blit(self.new_square.surf, self.new_square.rect)
            Squares_cliced.add(self)
            self.is_pressed = not self.is_pressed
        elif self.new_square:
            #self.surf.fill((0,0,255))
            Squares_cliced.remove(self)
            self.surf.fill(self.color)
            self.new_square.kill()
            self.is_pressed = not self.is_pressed


class Pice(pygame.sprite.Sprite):
    def __init__(self, color, path, square_id, name, pice_type):
        super(Pice, self).__init__()
        
        #self.surf = pygame.image.load("D:\\labs\\python_classes\\chess\\pices\\temp\\white_king.png").convert()
        self.surf = pygame.image.load(path + os.sep + color + f"_{name}.png").convert()
        self.surf.set_colorkey((255, 0, 0), RLEACCEL)
        #self.rect = self.surf.get_rect()
        self.rect = self.surf.get_rect(
            center=(
                BOARD_WIDTH/8/2,
                BOARD_WIDTH/8/2,
            )
        )
        self.sqare_id = square_id
        self.pice_type = pice_type
        self.color = color
        #print(self.pice_type)

    def make_a_move(self, new_position):
        self.sqare_id = new_position

    def pm(self, board):
        self.pice_type.find_moves(board)
        #print(self.pice_type.moves)
        return self.pice_type.convert_moves_for_GUI()