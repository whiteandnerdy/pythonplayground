import pygame
import glob
import sys
from pygame.locals import *

walk_left = {}
walk_right = {}

walk_left[1] = "resources/player-left_1.png"
walk_left[2] = "resources/player-left_2.png"
walk_left[3] = "resources/player-left_3.png"
walk_left[4] = "resources/player-left_4.png"
walk_left[5] = "resources/player-left_5.png"

walk_right[1] = "resources/player-right_1.png"
walk_right[2] = "resources/player-right_2.png"
walk_right[3] = "resources/player-right_3.png"
walk_right[4] = "resources/player-right_4.png"
walk_right[5] = "resources/player-right_5.png"


class Player:
    def __init__(self):
        self.x = 200
        self.y = 365
        self.ani_speed_init = 3  # higher number slower animation
        self.ani_speed = self.ani_speed_init
        self.ani = glob.glob("resources/player-right_*.png")  # player starts facing right
        self.ani.sort()
        self.ani_pos = 0
        self.ani_max = len(self.ani) - 1
        self.img = pygame.image.load(self.ani[0])
        self.update(0)

    def update(self, pos):
        if pos != 0:
            self.ani_speed -= 1
            self.x += pos
            if self.ani_speed == 0:
                self.img = pygame.image.load(self.ani[self.ani_pos])
                self.ani_speed = self.ani_speed_init
                if self.ani_pos == self.ani_max:
                    self.ani_pos = 0
                else:
                    self.ani_pos += 1
        screen.blit(self.img, (self.x, self.y))

w_height = 400
w_width = 600
screen = pygame.display.set_mode((w_width, w_height))
clock = pygame.time.Clock()
player1 = Player()
position = 0

while 1:
    screen.fill((255, 255, 255))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            player1.ani = glob.glob("resources/player-right_*.png")
            position = 1
        elif event.type == KEYUP and event.key == K_RIGHT:
            position = 0
        elif event.type == KEYDOWN and event.key == K_LEFT:
            player1.ani = glob.glob("resources/player-left_*.png")
            position = -1
        elif event.type == KEYUP and event.key == K_LEFT:
            position = 0

    player1.update(position)
    pygame.display.update()
