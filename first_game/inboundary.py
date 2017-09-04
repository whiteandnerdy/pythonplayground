class InBoundary:
    """Just keeps you from leaving the boundary box.  Sticks you to the boundary when you would overshoot.
    Informs whether you're on the boundary box or within it."""

    def __init__(self, boundary):
        self.boundary = boundary

    def stick_and_get_new_position(self, old_rect, new_rect, on_boundary):
        new_rect = new_rect.copy()

        if old_rect.left < self.boundary.left \
                or old_rect.right > self.boundary.right \
                or old_rect.top < self.boundary.top \
                or old_rect.bottom > self.boundary.bottom:
            raise Exception('old_rect not within or on the boundary.  old_rect, boundary = ', old_rect, self.boundary)

        if new_rect.left > self.boundary.left \
                and new_rect.right < self.boundary.right \
                and new_rect.top > self.boundary.top \
                and new_rect.bottom < self.boundary.bottom:
            # then you're wholly contained within the boundary and not on the boundaries
            return new_rect, False

        if new_rect.top <= self.boundary.top:
            new_rect.top = self.boundary.top
            on_boundary = True
        if new_rect.bottom >= self.boundary.bottom:
            new_rect.bottom = self.boundary.bottom
            on_boundary = True
        if new_rect.left <= self.boundary.left:
            new_rect.left = self.boundary.left
            on_boundary = True
        if new_rect.right >= self.boundary.right:
            new_rect.right = self.boundary.right
            on_boundary = True

        return new_rect, on_boundary
