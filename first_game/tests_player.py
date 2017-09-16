from collections import namedtuple
from pygame import K_LEFT, K_RIGHT, K_SPACE
from player import Player
import unittest


class Rect:
    def __init__(self, left, right, top, bottom):
        self.__left = left
        self.__right = right
        self.__top = top
        self.__bottom = bottom

        if left > right or top > bottom:
            raise Exception('invalid: ' + str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Rect: {{left = {}, right = {}, top = {}, bottom = {}}}' \
            .format(self.left, self.right, self.top, self.bottom)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__  # do property-wise comparison instead of object reference comparison

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, val):
        self.__right += val - self.__left
        self.__left = val

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, val):
        self.__left += val - self.__right
        self.__right = val

    @property
    def top(self):
        return self.__top

    @top.setter
    def top(self, val):
        self.__bottom += val - self.__top
        self.__top = val

    @property
    def bottom(self):
        return self.__bottom

    @bottom.setter
    def bottom(self, val):
        self.__top -= self.__bottom - val
        self.__bottom = val


class Layer:
    def __init__(self, boundary):
        self.boundary = boundary

    def collide(self, a, b):
        if self.boundary is None:
            return []
        else:
            return [self.boundary]


class Boundary:
    def __init__(self, left, right, top, bottom, property):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.property = property

    def __getitem__(self, item):
        return property

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Rect: {{left = {}, right = {}, top = {}, bottom = {}, property = {}}}' \
            .format(self.left, self.right, self.top, self.bottom, self.property)


class Player_Tests(unittest.TestCase):
    def test_the_space_key_begins_a_jump(self):
        vertical_velocity = Player._maintain_jump(key_pressed={K_RIGHT: False, K_LEFT: False, K_SPACE: True},
                                                  on_top=True, vertical_velocity=0, default_vertical_velocity=1000)
        self.assertEqual(vertical_velocity, -460)  # -500 + 40

    def test_can_not_jump_in_mid_air(self):
        vertical_velocity = Player._maintain_jump(key_pressed={K_RIGHT: False, K_LEFT: False, K_SPACE: True},
                                                  on_top=False, vertical_velocity=0, default_vertical_velocity=1000)
        self.assertEqual(vertical_velocity, 40)  # 0 + 40

    def test_can_not_resolve_collision_zone_when_any_point_is_inside_the_boundary(self):
        Rect = namedtuple('Rect', 'left right top bottom')
        with self.assertRaises(Exception):
            collision_zone = Player._get_collision_zone(boundary=Rect(10, 20, 10, 20), rect=Rect(4, 16, 14, 16))

    def test_can_not_resolve_collision_zone_when_rect_overlaps_boundary(self):
        Rect = namedtuple('Rect', 'left right top bottom')
        with self.assertRaises(Exception):
            # sliver through boundary
            collision_zone = Player._get_collision_zone(boundary=Rect(10, 20, 10, 20), rect=Rect(4, 26, 14, 16))
            print('incorrect:', collision_zone)
        with self.assertRaises(Exception):
            # bigger than boundary in every extent
            collision_zone = Player._get_collision_zone(boundary=Rect(10, 20, 10, 20), rect=Rect(4, 26, 4, 26))
            print('incorrect:', collision_zone)
        with self.assertRaises(Exception):
            # smaller than boundary in every extent
            collision_zone = Player._get_collision_zone(boundary=Rect(10, 20, 10, 20), rect=Rect(14, 16, 14, 16))
            print('incorrect:', collision_zone)

    # sticking tests


# I refactored some logic in Player to @staticmethod so I could avoid implementing the
# inherited dependencies of parent type Sprite in unit tests.

    def test_the_space_key_begins_a_jump(self):
        vertical_velocity = Player._maintain_jump(key_pressed={K_RIGHT: False, K_LEFT: False, K_SPACE: True},
                                                  on_top=True, vertical_velocity=0, default_vertical_velocity=1000,
                                                  on_boundary=False, can_go_higher=False)
        self.assertEqual(vertical_velocity, -500)

    def test_can_not_jump_in_mid_air(self):
        vertical_velocity = Player._maintain_jump(key_pressed={K_RIGHT: False, K_LEFT: False, K_SPACE: True},
                                                  on_top=False, vertical_velocity=0, default_vertical_velocity=1000,
                                                  on_boundary=False, can_go_higher=False)
        self.assertEqual(vertical_velocity, 40)  # 0 + 40


if __name__ == '__main__':
    unittest.main()
