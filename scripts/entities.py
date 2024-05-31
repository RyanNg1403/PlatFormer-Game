import pygame
import random
class PhysicsEntity:
    def __init__(self, game, e_type, pos):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.velocity = [0, 0]
        self.action = ''
        self.anim_offset = [0, -9.]
        self.flip = False
        self.size = (30,30)

        self.set_action('fall')

    def rect(self):
        player_rect =  pygame.Rect(self.pos[0],self.pos[1],self.size[0], self.size[1])
        player_rect.center = (self.pos[0],self.pos[1])
        return player_rect
    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
    
                
    def update(self, tilemap, movement=(0, 0)):
        movement = list(movement)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}



        frame_movement = (movement[0] * 1.5 + self.velocity[0], movement[1] * 1.5+ self.velocity[1])
        
        
        # Horizontal movement and collision
        self.pos[0] += frame_movement[0]
        # LEFT + RIGHT
        signs = {'left' : -1 , 'right': 1}
        for key in signs:
            entity_rect = self.rect()
            rects = tilemap.physics_rects_around((self.pos[0] + signs[key] *self.size[0]//2,self.pos[1]))
            # rects.sort(key = lambda rect: abs(entity_rect.centery - rect.centery) + abs(entity_rect.centerx - rect.centerx))
            for rect in rects:
                if entity_rect.colliderect(rect):
                    if frame_movement[0] > 0:
                        entity_rect.right = rect.left   
                        self.collisions['right'] = True
                        self.pos[0] = entity_rect.centerx
                        break
                        
                    if frame_movement[0] < 0:
                        entity_rect.left = rect.right
                        self.collisions['left'] = True
                        self.pos[0] = entity_rect.centerx
                        break
                    
        # Vertical movement and collision
        self.pos[1] += frame_movement[1]
        signs = {'top' : -1 , 'bottom': 1}
        for key in signs:
            entity_rect = self.rect()
            rects = tilemap.physics_rects_around((self.pos[0] ,self.pos[1] + signs[key] * self.size[1]//2 ))
            # rects.sort(key = lambda rect: abs(entity_rect.centery - rect.centery) + abs(entity_rect.centerx - rect.centerx))
            for rect in rects:
                if entity_rect.colliderect(rect):
                    if frame_movement[1] > 0:
        
                        entity_rect.bottom = rect.top  
                        self.collisions['down'] = True
                        self.pos[1] = entity_rect.centery 
                        break
                    if frame_movement[1] < 0:
                        entity_rect.top = rect.bottom
                        self.collisions['up'] = True
                        self.pos[1] = entity_rect.centery
                        break

        if movement[0] < 0:
            self.flip = True
        if movement[0] > 0:
            self.flip = False
        self.velocity[1] = min(self.velocity[1] + 0.1, 10)
        
        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0
        
      
        self.animation.update()
        # print(self.pos, movement, frame_movement, self.velocity[1])

    def render(self, surf, offset=(0, 0)):
        # Render the entity
        animation_img = self.animation.img()
        animation_rect = self.rect()
        animation_rect.center = (self.pos[0] - offset[0] + self.anim_offset[0],
                                 self.pos[1] - offset[1] + self.anim_offset[1])

        # Draw the bounding rectangle
        # pygame.draw.rect(surf, (255, 0, 0), animation_rect, 2)

        # Blit the animation
        surf.blit(pygame.transform.flip(animation_img, self.flip, False), animation_rect.topleft)

class Player(PhysicsEntity):
    def __init__(self, game, pos, type="player"):
        super().__init__(game, type, pos)
        self.air_time = 0
        self.jumps = 100
        self.dashes = 0
        self.crouching = False
        self.running_on_right = False

    def update(self, tilemap, movement):
        super().update(tilemap=tilemap, movement=movement)
        
        
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 3
        if self.air_time > 4 and self.velocity[1] < 0: 
            self.set_action('jump')
        elif self.air_time > 4 and self.velocity[1] > 0: 
            self.set_action('fall')
        elif movement[0] != 0: 
            self.set_action('run')
        elif self.crouching:
            self.set_action('crouch')
        else: 
            self.set_action('idle')
        


        if self.dashes > 0:
            self.dashes = max(self.dashes - 1, 0)
        else:
            self.dashes = min(self.dashes + 1, 0)

        if abs(self.dashes) > 50:
            self.velocity[0] = (abs(self.dashes) // self.dashes) * 8
            self.set_action('slide')
            if abs(self.dashes) == 51:
                self.velocity[0] *= 0.1

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def jump(self):
        if self.jumps >0:
            self.jumps -= 1
            self.velocity[1] -= 2
            self.air_time = 5

    def dash(self):
        if not self.dashes:
            if self.flip:
                self.dashes = -60
            else:
                self.dashes = 60
    def render(self, surf, offset, tilemap):
        # Render the entity
        animation_img = self.animation.img()
        animation_rect = self.rect()
        
        if self.action == 'run' and self.collisions['left']:

            animation_rect.center = (self.pos[0] - offset[0] -5,
                                   self.pos[1] - offset[1] + self.anim_offset[1])
        elif self.action == 'run' and self.collisions['right']:
            animation_rect.center = (self.pos[0] - offset[0] -10,
                                   self.pos[1] - offset[1] + self.anim_offset[1])
        else:
            animation_rect.center = (self.pos[0] - offset[0] ,
                                   self.pos[1] - offset[1] + self.anim_offset[1])

        # Draw the bounding rectangle
        # pygame.draw.rect(surf, (255, 0, 0), animation_rect,2)

        # Blit the animation
        
        surf.blit(pygame.transform.flip(animation_img, self.flip, False), animation_rect.topleft)
class Enemy(PhysicsEntity): 
    def __init__(self, game, pos, monster_type, e_type = 'enemy'): 
        self.monster_type = monster_type
        super().__init__(game,e_type,pos)
        self.size = [30,30]
        self.walking = 0 
        self.attack_montion = 0


        if self.monster_type == 'demon':
            self.anim_offsets = {'idle':[-20, -21], 'attack' : [-60, -45]}

        elif self.monster_type == 'horse': 
            self.anim_offsets = {'idle':[-5, -16], 'run' : [-5, -16], 'fall' : [-5,-16]}
        elif self.monster_type == 'ghost':
            self.anim_offsets = {'idle':[-5, -11], 'run' : [-5, -11], 'fall' : [-5,-11]}
    
    def update(self, tilemap , movement = (0,0)): 
        if self.monster_type == 'demon': 
            self.velocity[1] = 0

        if self.walking and self.monster_type in ['ghost', 'demon']:
            if not (self.collisions['left'] or self.collisions['right']):
                movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else: 
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

        elif self.walking and self.monster_type not in ['ghost', 'demon']:
            if tilemap.solid_check((self.rect().centerx + (-15 if self.flip else 15), self.pos[1] + 23)):
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
                    self.set_action('run')
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking: self.set_action('idle')
        elif random.random() < 0.01:
            self.walking = random.randint(30,120)

        if self.monster_type in ['demon', 'ghost']:
            if self.attack_montion:
                self.walking = 0
                self.attack_montion -= 1
                self.set_action('attack')
            else:
                self.set_action('idle')
                if random.random() > 0.995: 
                    self.attack_montion = 60 if self.monster_type != 'horse' else 0

        if self.anim_offset != self.anim_offsets[self.action]: 
            self.anim_offset = self.anim_offsets[self.action]
        super().update(tilemap=tilemap, movement=movement)

    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.monster_type+ '-' + self.action].copy()
    def render(self, surf, offset=(0, 0)):
        # Render the entity
        if self.monster_type == 'horse': 
            print(self.action)
        animation_img = self.animation.img()
        animation_rect = self.rect()
        if self.monster_type == 'demon' and not self.flip and self.action == 'attack':
            animation_rect.center = (self.pos[0] - offset[0] + self.anim_offset[0] + 43,
                                 self.pos[1] - offset[1] + self.anim_offset[1]+ 8)

        else: 
            animation_rect.center = (self.pos[0] - offset[0] + self.anim_offset[0],
                                 self.pos[1] - offset[1] + self.anim_offset[1])
        
        surf.blit(pygame.transform.flip(animation_img, self.flip, False), animation_rect.topleft)
