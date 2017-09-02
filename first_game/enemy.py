import pygame


class Enemy(pygame.sprite.Sprite):
    image = pygame.image.load('resources/enemy.png')

    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.last_direction = 'down'

    def update(self, dt, tilemap, keys_pressed, player):
        if self.last_direction == 'down':
            self.rect.y += 100 * dt
        else:
            self.rect.y -= 100 * dt

        colliding_cells = tilemap.layers['triggers'].collide(self.rect, 'blockers') + \
                          tilemap.layers['triggers'].collide(self.rect, 'reverse')

        if len(colliding_cells) > 0:
            cell = colliding_cells[0]

            # don't overshoot the boundary
            if self.last_direction == 'down':
                self.rect.bottom = cell.top
            else:
                self.rect.top = cell.bottom

            self.last_direction = 'up' if self.last_direction == 'down' else 'down'

        if self.rect.colliderect(player.rect):
            player.is_dead = True
