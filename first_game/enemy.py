import pygame
from outboundary import OutBoundary


class Enemy(pygame.sprite.Sprite):
    image = pygame.image.load('resources/enemy.png')

    def __init__(self, location, *groups):
        super().__init__(*groups)

        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.vertical_velocity = self.default_vertical_velocity = 400

    def update(self, dt, tilemap, keys_pressed, player):
        new_rect = self._get_new_position_without_boundaries(dt, self.rect, self.vertical_velocity)

        boundaries = [OutBoundary(boundary_object) for boundary_object in
                      tilemap.layers['triggers'].collide(new_rect, 'blockers')
                      if boundary_object['blockers'] == 'out']

        on_top = False
        for boundary in boundaries:
            new_rect, on_top = boundary.stick_and_get_new_position(self.rect, new_rect, on_top)

        self.vertical_velocity = self._maintain_jump(on_top, self.vertical_velocity, self.default_vertical_velocity)

        self.rect = new_rect

        if self.rect.colliderect(player.rect):
            player.is_dead = True

    @staticmethod
    def _get_new_position_without_boundaries(dt, new_rect, vertical_velocity):
        new_rect = new_rect.copy()

        new_rect.y += vertical_velocity * dt

        return new_rect

    @staticmethod
    def _maintain_jump(on_top, vertical_velocity, default_vertical_velocity):
        if on_top:  # don't jump from mid-air, you must be standing on top of something
            vertical_velocity = -500

        # turn jump into gravity over time by degrading the vertical velocity
        vertical_velocity = min(vertical_velocity + 40, default_vertical_velocity)
        return vertical_velocity
