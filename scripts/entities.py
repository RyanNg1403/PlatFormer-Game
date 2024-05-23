import pygame
class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos  = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.action = ''
        self.anim_offset = (-3,-3)
        self.flip = False
        self.set_action('idle')
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
    def update(self, tilemap,  movement = (0,0)):
        #Keep track of the type of the collison every iteration.
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        # Update the position of the player
        frame_movement = (movement[0] * 1.5 + self.velocity[0], movement[1] * 1.5 + self.velocity[1])

        #Check the collision for left-right movements.
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        #Check the collision for top-bottom movements.
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        # if the player falls, reset the velocity to zero.
        if self.collisions['up'] or self.collisions['down']: 
            self.velocity[1] = 0
        
        # Falling
        self.velocity[1] = min(self.velocity[1] + 0.1, 5)
        #Update animation
        if movement[0] < 0: 
            self.flip = True
        if movement[0]> 0: 
            self.flip = False

        self.animation.update()
    def render(self, surf, offset = (0,0)):
        # Render the window

        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False ), 
                  (self.pos[0] - offset[0] + self.anim_offset[0],
                  self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    
    def __init__(self, game, pos, size, type = "player"):
        super().__init__(game, type, pos, size)
        self.air_time = 0
    def update(self, tilemap, movement):
        super().update(tilemap=tilemap, movement=movement)
        self.air_time +=1
        if   self.collisions['down']: 
            self.air_time = 0   
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0: 
            self.set_action('run')
        else:
            self.set_action('idle')
        