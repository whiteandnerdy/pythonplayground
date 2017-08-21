from collections import namedtuple
from pygame import image, rect, key, K_LEFT, K_RIGHT, K_SPACE
from player import Player
import unittest


# I refactored some logic in Player to @staticmethod so I could avoid implementing the
# inherited dependencies of parent type Sprite in unit tests.

class PlayerTests(unittest.TestCase):
    def the_space_key_begins_a_jump(self):
        vertical_velocity = Player._maintain_jump(key_pressed={K_RIGHT: False, K_LEFT: False, K_SPACE: True},
                                                  on_top=True, vertical_velocity=0, default_vertical_velocity=1000)
        self.assertEqual(vertical_velocity, -460)  # -500 + 40

    def can_not_jump_in_mid_air(self):
        vertical_velocity = Player._maintain_jump(key_pressed={K_RIGHT: False, K_LEFT: False, K_SPACE: True},
                                                  on_top=False, vertical_velocity=0, default_vertical_velocity=1000)
        self.assertEqual(vertical_velocity, 40)  # 0 + 40

    def it(self):
        class Layer:
            def collide(self, a, b):
                return [Boundary()]

        class Boundary:
            left = 0
            right = 0
            bottom = 0
            top = 0

            def __getitem__(self, item):
                return 'tlrb'

        Rect = namedtuple('Rect', 'right left bottom top')
        new_rect, on_top = Player._get_new_position_considering_boundaries(Rect(0, 0, 0, 0), Rect(0, 0, 0, 0), Layer())


if __name__ == '__main__':
    unittest.main()
