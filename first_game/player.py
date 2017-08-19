import pygame

from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('resources/player-right.png')
        self.right_image = self.image
        self.left_image = pygame.image.load('resources/player-left.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0
        self.is_dead = False
        self.direction = 1
        self.bullet_delay = 2

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.image = self.left_image
            self.direction = -1
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.image = self.right_image
            self.direction = 1

        self.bullet_delay = min(self.bullet_delay + dt, 2)

        if key[pygame.K_LSHIFT] \
                and len([sprite for sprite in game.sprites if type(sprite) == Bullet]) < 5 \
                and self.bullet_delay > .1:
            if self.direction > 0:
                Bullet(self.rect.midright, 1, game.sprites)
                self.bullet_delay = 0
            else:
                Bullet(self.rect.midleft, -1, game.sprites)
                self.bullet_delay = 0

        if self.resting and key[pygame.K_SPACE]:
            self.dy = -500
        self.dy = min(400, self.dy + 40)

        self.rect.y += self.dy * dt

        new = self.rect
        self.resting = False
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            blockers = cell['blockers']
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0

        game.tilemap.set_focus(new.x, new.y)
