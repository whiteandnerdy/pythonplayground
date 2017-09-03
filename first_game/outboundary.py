class OutBoundary:
    def __init__(self, boundary):
        self.boundary = boundary

    def stick_and_get_new_position(self, old_rect, new_rect, on_top):
        new_rect = new_rect.copy()

        # Nobody says that on_top is False.  If anybody says it's True then it's True for everyone.
        collision_zone = self._get_collision_zone(old_rect)

        if collision_zone == 'NW':
            new_rect.bottom = self.boundary.top + 1
            new_rect.right = self.boundary.left
        elif collision_zone == 'N':
            new_rect.bottom = self.boundary.top
            on_top = True
        elif collision_zone == 'NE':
            new_rect.bottom = self.boundary.top + 1
            new_rect.left = self.boundary.right
        elif collision_zone == 'E':
            new_rect.left = self.boundary.right
        elif collision_zone == 'SE':
            new_rect.left = self.boundary.right
            new_rect.top = self.boundary.bottom - 1
        elif collision_zone == 'S':
            new_rect.top = self.boundary.bottom
        elif collision_zone == 'SW':
            new_rect.top = self.boundary.bottom - 1
            new_rect.right = self.boundary.left
        elif collision_zone == 'W':
            new_rect.right = self.boundary.left
        else:
            raise Exception('unknown collision_zone: ', collision_zone)

        return new_rect, on_top

    def _get_collision_zone(self, rect):
        if rect.right <= self.boundary.left and rect.bottom <= self.boundary.top:
            return 'NW'
        if rect.left >= self.boundary.right and rect.bottom <= self.boundary.top:
            return 'NE'
        if rect.right <= self.boundary.left and rect.top >= self.boundary.bottom:
            return 'SW'
        if rect.left >= self.boundary.right and rect.top >= self.boundary.bottom:
            return 'SE'
        if rect.bottom <= self.boundary.top:
            return 'N'
        if rect.right <= self.boundary.left:
            return 'W'
        if rect.left >= self.boundary.right:
            return 'E'
        if rect.top >= self.boundary.bottom:
            return 'S'
        raise Exception('can not resolve collision zone: {} in {}'.format(str(rect), str(self.boundary)))
