from pygame import image, rect, key, K_LEFT, K_RIGHT, K_SPACE
from pygame.sprite import Sprite
from collections import namedtuple


class Player(Sprite):
    def __init__(self, initial_location, *groups):
        super().__init__(*groups)

        Images = namedtuple('Images', 'right left')
        self.images = Images(image.load('resources/player-right.png'),
                             image.load('resources/player-left.png'))
        self.vertical_velocity = self.default_vertical_velocity = 400

        self.image = self.images.right
        self.rect = rect.Rect(initial_location, self.image.get_size())
        self.is_dead = False

    def update(self, dt, game):
        tilemap = game.tilemap
        key_pressed = key.get_pressed()

        new_rect = self._get_new_position_without_boundaries(
            dt, self.rect, key_pressed, self.vertical_velocity)

        new_rect, on_top = self._get_new_position_considering_boundaries(
            self.rect, new_rect, tilemap.layers['triggers'])

        self.vertical_velocity = self._maintain_jump(
            key_pressed, on_top, self.vertical_velocity, self.default_vertical_velocity)

        if key_pressed[K_RIGHT]:
            self.image = self.images.right
        if key_pressed[K_LEFT]:
            self.image = self.images.left

        self.rect = new_rect
        tilemap.set_focus(new_rect.x, new_rect.y) # move the viewport camera as necessary

    @staticmethod
    def _maintain_jump(key_pressed, on_top, vertical_velocity, default_vertical_velocity):
        if key_pressed[K_SPACE] and on_top:  # don't jump from mid-air, you must be standing on top of something
            vertical_velocity = -500

        # turn jump into gravity over time by degrading the vertical velocity
        vertical_velocity = min(vertical_velocity + 40, default_vertical_velocity)
        return vertical_velocity

    @staticmethod
    def _get_new_position_without_boundaries(dt, current_rect, key_pressed, vertical_velocity):
        new_rect = current_rect.copy()

        if key_pressed[K_LEFT]:
            new_rect.x -= 300 * dt
        if key_pressed[K_RIGHT]:
            new_rect.x += 300 * dt

        new_rect.y += vertical_velocity * dt

        return new_rect

    @staticmethod
    def _get_new_position_considering_boundaries(old_rect, new_rect, triggers_layer):
        on_top = False

        for boundary, properties in [(boundary, boundary['blockers']) for boundary
                                     in triggers_layer.collide(new_rect, 'blockers')]:
            if 'l' in properties and old_rect.right <= boundary.left and new_rect.right > boundary.left:
                new_rect.right = boundary.left
            if 'r' in properties and old_rect.left >= boundary.right and new_rect.left < boundary.right:
                new_rect.left = boundary.right
            if 't' in properties and old_rect.bottom <= boundary.top and new_rect.bottom > boundary.top:
                new_rect.bottom = boundary.top
                on_top = True
            if 'b' in properties and old_rect.top >= boundary.bottom and new_rect.top < boundary.bottom:
                new_rect.top = boundary.bottom

        return new_rect, on_top
