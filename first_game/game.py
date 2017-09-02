from pygame import key, event, QUIT, KEYDOWN, K_ESCAPE, display, time, image

from enemy import Enemy
from player import Player
from resources import tmx


class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.background = image.load('resources/background.png')

        self.tilemap = tmx.load('resources/map.tmx', screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.add_named(self.sprites, 'player')

        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.add_named(self.enemies, 'enemies')

        # change the paint order so that foreground terrain is painted last
        foreground_terrain = self.tilemap.layers.pop(self.tilemap.layers.index(self.tilemap.layers['Tile Layer 2']))
        self.tilemap.layers.add_named(foreground_terrain, 'foreground_terrain')

    def main(self):
        clock = time.Clock()
        while 1:
            dt = clock.tick(30)

            for _event in event.get():
                if _event.type == QUIT:
                    return
                if _event.type == KEYDOWN and _event.key == K_ESCAPE:
                    return

            self.tilemap.update(dt / 1000., self.tilemap, key.get_pressed(), self.player)
            self.screen.blit(self.background, (0, 0))
            self.tilemap.draw(self.screen)
            display.flip()

            if self.player.is_dead:
                print('YOU DIED')
                return
