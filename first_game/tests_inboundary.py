from collections import namedtuple
from inboundary import InBoundary
import unittest


class Rect:
    def __init__(self, left, right, top, bottom):
        self.__left = left
        self.__right = right
        self.__top = top
        self.__bottom = bottom

        if left > right or top > bottom:
            raise Exception('invalid: ' + str(self))

    def copy(self):
        return self

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


class InBoundary_Tests(unittest.TestCase):
    boundary_rect = Rect(10, 20, 10, 20)
    center_rect = Rect(14, 16, 14, 16)

    def test_error_if_old_rect_not_in_or_on_boundary_box(self):
        with self.assertRaises(Exception):
            new_rect, on_boundary = InBoundary(boundary=self.boundary_rect) \
                .stick_and_get_new_position(old_rect=Rect(1, 3, 1, 3), new_rect=Rect(12, 14, 12, 14), on_boundary=False)

    def test_sticking(self):
        Assertion = namedtuple('Assertion', 'new_rect rect on_boundary, test_name')

        assertions = [
            Assertion(Rect(12, 14, 12, 14), Rect(12, 14, 12, 14), False, 'test_new_position_not_altered_when_not_colliding_box_edges')
            ,Assertion(Rect(14, 16, 4, 6), Rect(14, 16, 10, 12), True, 'test_colliding_top_boundary_sticks_top')
            ,Assertion(Rect(14, 16, 24, 26), Rect(14, 16, 18, 20), True, 'test_colliding_bottom_boundary_sticks_bottom')
            ,Assertion(Rect(4, 6, 14, 16), Rect(10, 12, 14, 16), True, 'test_colliding_left_boundary_sticks_left')
            ,Assertion(Rect(24, 26, 14, 16), Rect(18, 20, 14, 16), True, 'test_colliding_right_boundary_sticks_right')
            ,Assertion(Rect(4, 6, 4, 6), Rect(10, 12, 10, 12), True, 'test_colliding_topleft_sticks_top_and_left')
            ,Assertion(Rect(10, 12, 14, 16), Rect(10, 12, 14, 16), True, 'test_not_overshooting_sets_on_boundary_True')
        ]

        for assertion in assertions:
            new_rect, on_boundary = InBoundary(boundary=self.boundary_rect) \
                .stick_and_get_new_position(old_rect=self.center_rect, new_rect=assertion.new_rect, on_boundary=False)

            self.assertEqual(new_rect, assertion.rect)
            self.assertEqual(on_boundary, assertion.on_boundary)


if __name__ == '__main__':
    unittest.main()
