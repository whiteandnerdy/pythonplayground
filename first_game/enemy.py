from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame import image
from inboundary import InBoundary
from outboundary import OutBoundary


class Enemy(Sprite):
    image = image.load('resources/enemy.png')

    def __init__(self, location, *groups):
        super().__init__(*groups)

        self.rect = Rect(location, self.image.get_size())
        self.vertical_velocity = self.default_vertical_velocity = 400

    def update(self, dt, tilemap, keys_pressed, player):
        new_rect = self._get_new_position_without_boundaries(dt, self.rect, self.vertical_velocity)

        in_boundaries = [InBoundary(boundary_object) for boundary_object in
                      tilemap.layers['triggers'].collide(new_rect, 'blockers')
                      if boundary_object['blockers'] == 'in']
        out_boundaries = [OutBoundary(boundary_object) for boundary_object in
                      tilemap.layers['triggers'].collide(new_rect, 'blockers')
                      if boundary_object['blockers'] == 'out']

        on_top = False
        on_boundary = False
        for boundary in in_boundaries:
            new_rect, on_boundary = boundary.stick_and_get_new_position(self.rect, new_rect, on_boundary)
        for boundary in out_boundaries:
            new_rect, on_boundary, on_top = boundary.stick_and_get_new_position(self.rect, new_rect,
                                                                                on_boundary, on_top)

        self.vertical_velocity = self._maintain_jump(
            on_boundary, self.vertical_velocity, self.default_vertical_velocity, new_rect.top - self.rect.top > 0)

        self.rect = new_rect

        if self.rect.colliderect(player.rect):
            player.is_dead = True

    @staticmethod
    def _get_new_position_without_boundaries(dt, new_rect, vertical_velocity):
        new_rect = new_rect.copy()

        new_rect.y += vertical_velocity * dt

        return new_rect

    @staticmethod
    def _maintain_jump(on_boundary, vertical_velocity, default_vertical_velocity, can_go_higher):
        if on_boundary and vertical_velocity == default_vertical_velocity:  # don't jump from mid-air, you must be standing on top of something
            return -500

        # stop velocity degrading short when you bump your head
        if on_boundary and vertical_velocity != default_vertical_velocity and not can_go_higher:
            return default_vertical_velocity

        # turn jump into gravity over time by degrading the vertical velocity
        return min(vertical_velocity + 40, default_vertical_velocity)
