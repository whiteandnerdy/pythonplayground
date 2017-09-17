from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame import image
from inboundary import InBoundary
from outboundary import OutBoundary
from random import randint


class Enemy(Sprite):
    image = image.load('resources/enemy.png')

    def __init__(self, location, *groups):
        super().__init__(*groups)

        self.rect = Rect(location, self.image.get_size())
        self.vertical_velocity = self.default_vertical_velocity = 200
        self.rightward_velocity = 1
        self.vertical_velocity_decay = 40
        self.jump_velocity = -300

    def update(self, dt, tilemap, keys_pressed, player):
        new_rect = self._get_new_position_without_boundaries(dt, self.rect,
                                                             self.vertical_velocity, self.rightward_velocity)

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

        if on_boundary:
            self.rightward_velocity = randint(-100, 100)
            self.vertical_velocity_decay = randint(5, 30)
            self.jump_velocity = randint(-500, -300)

        self.vertical_velocity = self._maintain_jump(
            on_boundary, self.vertical_velocity, self.default_vertical_velocity,
            self.vertical_velocity_decay, self.jump_velocity,
            can_go_higher=self.rect.top - new_rect.top > 0,
            can_go_lower=self.rect.top - new_rect.top < 0)

        self.rect = new_rect

        if self.rect.colliderect(player.rect):
            player.is_dead = True

    @staticmethod
    def _get_new_position_without_boundaries(dt, new_rect, vertical_velocity, rightward_velocity):
        new_rect = new_rect.copy()

        new_rect.y += vertical_velocity * dt
        new_rect.x += rightward_velocity * dt

        return new_rect

    @staticmethod
    def _maintain_jump(on_boundary, vertical_velocity, default_vertical_velocity,
                       vertical_velocity_decay, jump_velocity, can_go_higher, can_go_lower):
        if on_boundary and not can_go_lower and vertical_velocity == default_vertical_velocity:  # don't jump from mid-air, you must be standing on top of something
            return jump_velocity

        # stop velocity degrading short when you bump your head
        if on_boundary and vertical_velocity != default_vertical_velocity and not can_go_higher:
            return default_vertical_velocity

        # turn jump into gravity over time by degrading the vertical velocity
        return min(vertical_velocity + vertical_velocity_decay, default_vertical_velocity)
