from pygame import image, rect, K_LEFT, K_RIGHT, K_SPACE
from pygame.sprite import Sprite
from glob import glob
from playeranimation import PlayerAnimation
from outboundary import OutBoundary


class Player(Sprite):
    def __init__(self, initial_location, *groups):
        super().__init__(*groups)

        self.vertical_velocity = self.default_vertical_velocity = 400

        self.animation = PlayerAnimation(
            right_images=[image.load(path) for path in sorted(glob("resources/player-right_*.png"))],
            left_images=[image.load(path) for path in sorted(glob("resources/player-left_*.png"))])
        self.image = self.animation.right_images[0]

        self.rect = rect.Rect(initial_location, self.image.get_size())
        self.is_dead = False

    def update(self, dt, tilemap, keys_pressed, player):
        new_rect = self._get_new_position_without_boundaries(
            dt, self.rect, keys_pressed, self.vertical_velocity)

        boundaries = [OutBoundary(boundary_object) for boundary_object in
                      tilemap.layers['triggers'].collide(new_rect, 'blockers')
                      if boundary_object['blockers'] == 'out']

        on_top = False
        on_boundary = False
        for boundary in boundaries:
            new_rect, on_boundary, on_top = boundary.stick_and_get_new_position(self.rect, new_rect,
                                                                                on_boundary, on_top)

        self.vertical_velocity = self._maintain_jump(
            keys_pressed, on_top, self.vertical_velocity, self.default_vertical_velocity,
            on_boundary, self.rect.top - new_rect.top > 0)

        new_image = self.animation.update(dt, keys_pressed, on_top)
        if new_image is not None:
            self.image = new_image

        self.rect = new_rect
        tilemap.set_focus(new_rect.x, new_rect.y) # move the viewport camera as necessary

        if new_rect.bottom > 3300:
            self.is_dead = True

    @staticmethod
    def _maintain_jump(key_pressed, on_top, vertical_velocity, default_vertical_velocity, on_boundary, can_go_higher):
        if key_pressed[K_SPACE] and on_top:  # don't jump from mid-air, you must be standing on top of something
            return -500

        # stop velocity degrading short when you bump your head
        if on_boundary and vertical_velocity != default_vertical_velocity and not can_go_higher:
            print(can_go_higher)
            return default_vertical_velocity

        # turn jump into gravity over time by degrading the vertical velocity
        return min(vertical_velocity + 40, default_vertical_velocity)

    @staticmethod
    def _get_new_position_without_boundaries(dt, new_rect, key_pressed, vertical_velocity):
        new_rect = new_rect.copy()

        if key_pressed[K_LEFT]:
            new_rect.x -= 250 * dt
        if key_pressed[K_RIGHT]:
            new_rect.x += 250 * dt

        new_rect.y += vertical_velocity * dt

        return new_rect
