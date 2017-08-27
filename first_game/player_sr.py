from pygame import image, rect, key, K_LEFT, K_RIGHT, K_SPACE
from pygame.sprite import Sprite
from collections import namedtuple
from itertools import cycle
from glob import glob

class Player_SR(Sprite):
    def __init__(self, initial_location, *groups):
        super().__init__(*groups)

        Images = namedtuple('Images', 'right left')
        self.right_images = [image.load(path) for path in sorted(glob("resources/player-right_*.png"))]
        self.left_images = [image.load(path) for path in sorted(glob("resources/player-left_*.png"))]
        self.images = Images(cycle(self.right_images), cycle(self.left_images))

        self.vertical_velocity = self.default_vertical_velocity = 400

        self.image = next(self.images.right)
        self.rect = rect.Rect(initial_location, self.image.get_size())
        self.is_dead = False
        self.last_direction = 'right'
        self.animation_pause_ms = 50
        self.ms_since_animation_change = 0

    def update(self, dt, game):
        tilemap = game.tilemap
        keys_pressed = key.get_pressed()

        self.ms_since_animation_change += dt * 1000

        new_rect = self._get_new_position_without_boundaries(
            dt, self.rect, keys_pressed, self.vertical_velocity)

        new_rect, on_top = self._stick_and_get_new_position(
            self.rect, new_rect, tilemap.layers['triggers'])

        self.vertical_velocity = self._maintain_jump(
            keys_pressed, on_top, self.vertical_velocity, self.default_vertical_velocity)

        if keys_pressed[K_RIGHT] and on_top:
            if self.ms_since_animation_change >= self.animation_pause_ms:
                self.ms_since_animation_change = 0
                self.image = next(self.images.right)
                self.last_direction = 'right'
        if keys_pressed[K_LEFT] and on_top:
            if self.ms_since_animation_change >= self.animation_pause_ms:
                self.ms_since_animation_change = 0
                self.image = next(self.images.left)
                self.last_direction = 'left'
        if keys_pressed[K_RIGHT] and not on_top:
            self.image = self.right_images[0]
            self.last_direction = 'right'
        if keys_pressed[K_LEFT] and not on_top:
            self.image = self.left_images[0]
            self.last_direction = 'left'
        if keys_pressed[K_SPACE] and on_top:  # if you're launching a jump
            self.image = self.right_images[0] if self.last_direction == 'right' else self.left_images[0]

        self.rect = new_rect
        tilemap.set_focus(new_rect.x, new_rect.y) # move the viewport camera as necessary

        if new_rect.bottom > 3300:
            self.is_dead = True

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
    def _get_collision_zone(boundary, rect):
        if rect.right <= boundary.left and rect.bottom <= boundary.top:
            return 'NW'
        if rect.left >= boundary.right and rect.bottom <= boundary.top:
            return 'NE'
        if rect.right <= boundary.left and rect.top >= boundary.bottom:
            return 'SW'
        if rect.left >= boundary.right and rect.top >= boundary.bottom:
            return 'SE'
        if rect.bottom <= boundary.top:
            return 'N'
        if rect.right <= boundary.left:
            return 'W'
        if rect.left >= boundary.right:
            return 'E'
        if rect.top >= boundary.bottom:
            return 'S'
        raise Exception('can not resolve collision zone: {} in {}'.format(str(rect), str(boundary)))

    @staticmethod
    def _stick_and_get_new_position(old_rect, new_rect, triggers_layer):
        boundaries_and_properties = \
            [(boundary, boundary['blockers']) for boundary in triggers_layer.collide(new_rect, 'blockers')]

        if not any(boundaries_and_properties):
            return new_rect, False  # if you didn't collide with a boundary you can't be standing on anything

        on_top = False
        for boundary, property in boundaries_and_properties:
            collision_zone = Player_SR._get_collision_zone(boundary, old_rect)

            if collision_zone == 'NW':
                new_rect.bottom = boundary.top + 1
                new_rect.right = boundary.left
            elif collision_zone == 'N':
                new_rect.bottom = boundary.top
                on_top = True
            elif collision_zone == 'NE':
                new_rect.bottom = boundary.top + 1
                new_rect.left = boundary.right
            elif collision_zone == 'E':
                new_rect.left = boundary.right
            elif collision_zone == 'SE':
                new_rect.left = boundary.right
                new_rect.top = boundary.bottom - 1
            elif collision_zone == 'S':
                new_rect.top = boundary.bottom
            elif collision_zone == 'SW':
                new_rect.top = boundary.bottom - 1
                new_rect.right = boundary.left
            elif collision_zone == 'W':
                new_rect.right = boundary.left
            else:
                raise Exception('unknown collision_zone: ', collision_zone)

        return new_rect, on_top
