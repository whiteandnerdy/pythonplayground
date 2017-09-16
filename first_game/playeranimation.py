from pygame import K_LEFT, K_RIGHT, K_SPACE
from collections import namedtuple
from itertools import cycle


class PlayerAnimation:
    """assumes the first image is the neutral, non-transitory image for right_images and left_images"""
    def __init__(self, right_images, left_images):
        Images = namedtuple('Images', 'right left')
        self.right_images = right_images
        self.left_images = left_images
        self.images = Images(cycle(self.right_images), cycle(self.left_images))
        self.last_direction = 'right'
        self.animation_pause_ms = 50
        self.ms_since_animation_change = 0

    def update(self, dt, keys_pressed, on_top):
        self.ms_since_animation_change += dt * 1000

        if keys_pressed[K_RIGHT] and on_top:
            if self.ms_since_animation_change >= self.animation_pause_ms:
                self.ms_since_animation_change = 0
                self.last_direction = 'right'
                return next(self.images.right)
        if keys_pressed[K_LEFT] and on_top:
            if self.ms_since_animation_change >= self.animation_pause_ms:
                self.ms_since_animation_change = 0
                self.last_direction = 'left'
                return next(self.images.left)
        if keys_pressed[K_RIGHT] and not on_top:
            self.last_direction = 'right'
            return self.right_images[0]
        if keys_pressed[K_LEFT] and not on_top:
            self.last_direction = 'left'
            return self.left_images[0]
        if keys_pressed[K_SPACE] and on_top:  # if you're launching a jump
            return self.right_images[0] if self.last_direction == 'right' else self.left_images[0]
