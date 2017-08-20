from pygame import image, rect, key, K_LEFT, K_RIGHT, K_SPACE
from player import Player
import unittest


# I refactored some logic in Player to @staticmethod so I could avoid implementing the
# inherited dependencies of parent type Sprite.

class PlayerTests(unittest.TestCase):
    def the_space_key_begins_a_jump(self):
        vertical_velocity = Player._maintain_jump(key_pressed={K_RIGHT: False, K_LEFT: False, K_SPACE: True},
                                                  on_top=True, vertical_velocity=0, default_vertical_velocity=1000)
        self.assertEqual(vertical_velocity, -460)  # -500 discounted 40


if __name__ == '__main__':
    unittest.main()
