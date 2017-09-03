from collections import namedtuple
from outboundary import OutBoundary
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


class OutBoundary_Tests(unittest.TestCase):
    def test_collision_zones(self):
        Assertion = namedtuple('Assertion', 'boundary rect zone test_name')

        assertions = \
            [
                Assertion(Rect(10, 20, 10, 20), Rect(4, 6, 4, 6), 'NW', 'test_player_landing_from_northwest_should_resolve_to_zone_NW')
                ,Assertion(Rect(10, 20, 10, 20), Rect(14, 16, 4, 6), 'N', 'test_player_landing_from_north_should_resolve_to_zone_N')
                ,Assertion(Rect(10, 20, 10, 20), Rect(24, 26, 4, 6), 'NE', 'test_player_landing_from_northeast_should_resolve_to_zone_NE')
                ,Assertion(Rect(10, 20, 10, 20), Rect(24, 26, 14, 16), 'E', 'test_player_landing_from_east_should_resolve_to_zone_E')
                ,Assertion(Rect(10, 20, 10, 20), Rect(24, 26, 24, 26), 'SE', 'test_player_landing_from_southeast_should_resolve_to_zone_SE')
                ,Assertion(Rect(10, 20, 10, 20), Rect(14, 16, 24, 26), 'S', 'test_player_landing_from_south_should_resolve_to_zone_S')
                ,Assertion(Rect(10, 20, 10, 20), Rect(4, 6, 24, 26), 'SW', 'test_player_landing_from_southwest_should_resolve_to_zone_SW')
                ,Assertion(Rect(10, 20, 10, 20), Rect(4, 6, 14, 16), 'W', 'test_player_landing_from_west_should_resolve_to_zone_W')
                ,Assertion(Rect(10, 20, 10, 20), Rect(4, 16, 4, 6), 'N', 'test_player_landing_from_northwest_and_north_should_resolve_to_zone_N')
                ,Assertion(Rect(10, 20, 10, 20), Rect(14, 26, 4, 6), 'N', 'test_player_landing_from_north_and_northeast_should_resolve_to_zone_N')
                ,Assertion(Rect(10, 20, 10, 20), Rect(4, 16, 24, 26), 'S', 'test_player_landing_from_southwest_and_south_should_resolve_to_zone_S')
                ,Assertion(Rect(10, 20, 10, 20), Rect(14, 26, 24, 26), 'S', 'test_player_landing_from_south_and_southeast_should_resolve_to_zone_S')
                ,Assertion(Rect(10, 20, 10, 20), Rect(4, 6, 14, 26), 'W', 'test_player_landing_from_west_and_southwest_should_resolve_to_zone_W')
                ,Assertion(Rect(10, 20, 10, 20), Rect(4, 6, 4, 16), 'W', 'test_player_landing_from_northwest_and_west_should_resolve_to_zone_W')
                ,Assertion(Rect(10, 20, 10, 20), Rect(24, 26, 4, 16), 'E', 'test_player_landing_from_east_and_northeast_should_resolve_to_zone_E')
                ,Assertion(Rect(10, 20, 10, 20), Rect(24, 26, 14, 26), 'E', 'test_player_landing_from_southeast_and_east_should_resolve_to_zone_E')
                ,Assertion(Rect(10, 20, 10, 20), Rect(0, 10, 0, 10), 'NW', 'test_player_landing_exactly_on_the_NW_corner_should_resolve_to_zone_NW')
                ,Assertion(Rect(10, 20, 10, 20), Rect(20, 30, 0, 10), 'NE', 'test_player_landing_exactly_on_the_NE_corner_should_resolve_to_zone_NE')
                ,Assertion(Rect(10, 20, 10, 20), Rect(0, 10, 20, 30), 'SW', 'test_player_landing_exactly_on_the_SW_corner_should_resolve_to_zone_SW')
                ,Assertion(Rect(10, 20, 10, 20), Rect(20, 30, 20, 30), 'SE', 'test_player_landing_exactly_on_the_SE_corner_should_resolve_to_zone_SE')
            ]

        for assertion in assertions:
            collision_zone = OutBoundary(assertion.boundary)._get_collision_zone(assertion.rect)
            self.assertEqual(collision_zone, assertion.zone, msg=assertion.test_name)

    def test_on_top_True_if_first_boundary_True(self):
        boundaries = [OutBoundary(boundary=Rect(10, 20, 10, 20)), OutBoundary(boundary=Rect(10, 20, 10, 20))]
        boundaries[0]._get_collision_zone = lambda rect: 'N'  # sets on_top = True
        boundaries[1]._get_collision_zone = lambda rect: 'S'  # does not set on_top

        on_top = False
        new_rect = Rect(10, 20, 10, 20)
        for boundary in boundaries:
            new_rect, on_top = boundary.stick_and_get_new_position(Rect(10, 20, 10, 20), new_rect, on_top)

        self.assertEqual(on_top, True)

    def test_on_top_True_if_second_boundary_True(self):
        boundaries = [OutBoundary(boundary=Rect(10, 20, 10, 20)), OutBoundary(boundary=Rect(10, 20, 10, 20))]
        boundaries[0]._get_collision_zone = lambda rect: 'S'  # sets on_top = True
        boundaries[1]._get_collision_zone = lambda rect: 'N'  # does not set on_top

        on_top = False
        new_rect = Rect(10, 20, 10, 20)
        for boundary in boundaries:
            new_rect, on_top = boundary.stick_and_get_new_position(Rect(10, 20, 10, 20), new_rect, on_top)

        self.assertEqual(on_top, True)

    def test_no_collision_means_not_on_top_and_new_rect_unchanged(self):
        original_rect = Rect(5, 7, 5, 7)
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(4, 6, 4, 6), new_rect=original_rect,
            on_top=False)
        self.assertEqual(on_top, False)
        self.assertEqual(new_rect, original_rect)

    def test_a_NW_collision_causes_a_W_stick_and_not_on_top(self):
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(4, 6, 4, 6), new_rect=Rect(14, 16, 14, 16),
            on_top=False)
        self.assertEqual(new_rect, Rect(8, 10, 9, 11))
        collision_zone = OutBoundary(Rect(10, 20, 10, 20))._get_collision_zone(new_rect)
        self.assertEqual(collision_zone, 'W')
        self.assertEqual(on_top, False)

    def test_a_N_collision_causes_a_N_stick_and_on_top(self):
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(14, 16, 4, 6), new_rect=Rect(14, 16, 14, 16),
            on_top=False)
        self.assertEqual(new_rect, Rect(14, 16, 8, 10))
        collision_zone = OutBoundary(Rect(10, 20, 10, 20))._get_collision_zone(new_rect)
        self.assertEqual(collision_zone, 'N')
        self.assertEqual(on_top, True)

    def test_a_NE_collision_causes_a_E_stick_and_not_on_top(self):
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(24, 26, 4, 6), new_rect=Rect(14, 16, 14, 16),
            on_top=False)
        self.assertEqual(new_rect, Rect(20, 22, 9, 11))
        collision_zone = OutBoundary(Rect(10, 20, 10, 20))._get_collision_zone(new_rect)
        self.assertEqual(collision_zone, 'E')
        self.assertEqual(on_top, False)

    def test_a_E_collision_causes_a_E_stick_and_not_on_top(self):
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(24, 26, 14, 16), new_rect=Rect(14, 16, 14, 16),
            on_top=False)
        self.assertEqual(new_rect, Rect(20, 22, 14, 16))
        collision_zone = OutBoundary(Rect(10, 20, 10, 20))._get_collision_zone(new_rect)
        self.assertEqual(collision_zone, 'E')
        self.assertEqual(on_top, False)

    def test_a_SE_collision_causes_a_E_stick_and_not_on_top(self):
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(24, 26, 24, 26), new_rect=Rect(14, 16, 14, 16),
            on_top=False)
        self.assertEqual(new_rect, Rect(20, 22, 19, 21))
        collision_zone = OutBoundary(Rect(10, 20, 10, 20))._get_collision_zone(new_rect)
        self.assertEqual(collision_zone, 'E')
        self.assertEqual(on_top, False)

    def test_a_S_collision_causes_a_S_stick_and_not_on_top(self):
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(14, 16, 24, 26), new_rect=Rect(14, 16, 14, 16),
            on_top=False)
        self.assertEqual(new_rect, Rect(14, 16, 20, 22))
        collision_zone = OutBoundary(Rect(10, 20, 10, 20))._get_collision_zone(new_rect)
        self.assertEqual(collision_zone, 'S')
        self.assertEqual(on_top, False)

    def test_a_SW_collision_causes_a_W_stick_and_not_on_top(self):
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(4, 6, 24, 26), new_rect=Rect(14, 16, 14, 16),
            on_top=False)
        self.assertEqual(new_rect, Rect(8, 10, 19, 21))
        collision_zone = OutBoundary(Rect(10, 20, 10, 20))._get_collision_zone(new_rect)
        self.assertEqual(collision_zone, 'W')
        self.assertEqual(on_top, False)

    def test_a_W_collision_causes_a_W_stick_and_not_on_top(self):
        new_rect, on_top = OutBoundary(boundary=Rect(10, 20, 10, 20)).stick_and_get_new_position(
            old_rect=Rect(4, 6, 14, 16), new_rect=Rect(14, 16, 14, 16),
            on_top=False)
        self.assertEqual(new_rect, Rect(8, 10, 14, 16))
        collision_zone = OutBoundary(Rect(10, 20, 10, 20))._get_collision_zone(new_rect)
        self.assertEqual(collision_zone, 'W')
        self.assertEqual(on_top, False)


if __name__ == '__main__':
    unittest.main()
