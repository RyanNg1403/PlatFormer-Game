import pygame
import random
from scripts.utils import add_color_overlay
pygame.mixer.pre_init(44100, -16, 512)  


pygame.mixer.init()
class PhysicsEntity:
    def __init__(self, game, e_type, pos, health):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.velocity = [0, 0]
        self.action = ''
        self.anim_offset = [0, -9.]
        self.flip = False
        self.size = (30, 30)
        self.health = health
        self.max_health = health

        self.set_action('fall')

    def rect(self):
        player_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        player_rect.center = (self.pos[0], self.pos[1])
        return player_rect

    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        movement = list(movement)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] * 1.5 + self.velocity[0], movement[1] * 1.5 + self.velocity[1])

        # Horizontal movement and collision
        self.pos[0] += frame_movement[0]
        signs = {'left': -1, 'right': 1}
        for key in signs:
            entity_rect = self.rect()
            rects = tilemap.physics_rects_around((self.pos[0] + signs[key] * self.size[0] // 2, self.pos[1]))
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
        signs = {'top': -1, 'bottom': 1}
        for key in signs:
            entity_rect = self.rect()
            rects = tilemap.physics_rects_around((self.pos[0], self.pos[1] + signs[key] * self.size[1] // 2))
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

    def render(self, surf, offset=(0, 0)):
        animation_img = self.animation.img()
        animation_rect = self.rect()
        animation_rect.center = (self.pos[0] - offset[0] + self.anim_offset[0],
                                 self.pos[1] - offset[1] + self.anim_offset[1])
        surf.blit(pygame.transform.flip(animation_img, self.flip, False), animation_rect.topleft)

        self.render_health_bar(surf, offset)

    def render_health_bar(self, surf, offset):
        health_bar_width = 25 if self.type == 'enemy' else 45
        health_bar_height = 5 if self.type == 'enemy' else 8 
        health_ratio = self.health / self.max_health
        player_health_bar = (35, 125, 75)
        if self.type == 'player': 
            if  0.3 <= health_ratio < 0.7: 
                player_health_bar = (135, 117, 27)
            elif health_ratio < 0.3:
                player_health_bar = (171, 83, 36)

        health_color = (255, 0, 0) if self.type == 'enemy' else player_health_bar  # Red color

        if self.type == 'player':
            bar_x = 10
            bar_y = 10
        else:
            if not self.flip:
                if self.monster_type == 'horse':
                    bar_x = self.pos[0] - offset[0] - health_bar_width // 2 + 15
                elif self.monster_type == 'demon': 
                    bar_x = self.pos[0] - offset[0] - health_bar_width // 2 + 20
                else:
                    bar_x = self.pos[0] - offset[0] - health_bar_width // 2 
            else:
                bar_x = self.pos[0] - offset[0] - health_bar_width // 2 
            bar_y = self.pos[1] - offset[1] - self.size[1] // 2 - 10

        pygame.draw.rect(surf, (0, 0, 0), (bar_x, bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(surf, health_color, (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))

class Player(PhysicsEntity):
    def __init__(self, game, pos, type="player"):
        super().__init__(game, type, pos, 100)  # Player with 100 HP
        self.air_time = 5
        self.jumps = 100
        self.dashes = 0
        self.crouching = False
        self.running_on_right = False
        self.attack = False
        self.dash_sound = pygame.mixer.Sound('data/sfx/dash.wav')
        self.attack_sound = pygame.mixer.Sound('data/sfx/hit.wav')
        self.run_sound = pygame.mixer.Sound('data/sfx/run.mp3')
        self.jump_sound = pygame.mixer.Sound('data/sfx/jump.mp3')
        self.land_sound = pygame.mixer.Sound('data/sfx/land.mp3')
        self.hurt_sound = pygame.mixer.Sound('data/sfx/hurt.mp3')
        self.die_sound = pygame.mixer.Sound('data/sfx/die.mp3')

    def update(self, tilemap, movement):
        super().update(tilemap=tilemap, movement=movement)
        self.air_time +=1
        if self.health <= 0: 
            self.set_action('die')
            self.animation.update()
            channel7.play(self.die_sound)
            return 
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 3
        if self.air_time > 4 and self.velocity[1] < 0: 
            if self.action != 'jump' and not channel4.get_busy(): 
                channel4.play(self.jump_sound)
            
            self.set_action('jump')
        elif self.air_time > 4 and self.velocity[1] > 0: 
            self.set_action('fall')
        elif movement[0] != 0: 
            self.set_action('run')
        elif self.crouching:
            self.set_action('crouch')
        elif self.attack:
            self.set_action('attack')
        else:
            if self.action == 'fall' and not channel5.get_busy(): 
                channel5.play(self.land_sound)
            self.set_action('idle')

        if self.dashes > 0:
            self.dashes = max(self.dashes - 1, 0)
        else:
            self.dashes = min(self.dashes + 1, 0)

        if abs(self.dashes) > 50:
            channel0.play(self.dash_sound)
            self.velocity[0] = (abs(self.dashes) // self.dashes) * 8
            self.set_action('slide')
            if abs(self.dashes) == 51:
                self.velocity[0] *= 0.1

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
        if self.action == 'attack':
            if not channel2.get_busy():
                channel2.play(self.attack_sound)
            self.anim_offset[0] = -15
        else: 
            self.anim_offset[0] = 0
            if self.action != 'run':
                channel3.stop()

                if not channel3.get_busy():
                    channel3.play(self.run_sound)
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
    def render(self, surf, offset):
        # Render the entity
        animation_img = self.animation.img()
        animation_rect = self.rect()
        
        if self.action == 'run' and self.collisions['left']:

            animation_rect.center = (self.pos[0] - offset[0] -5 + self.anim_offset[0],
                                   self.pos[1] - offset[1] + self.anim_offset[1])
        elif self.action == 'run' and self.collisions['right']:
            animation_rect.center = (self.pos[0] - offset[0] -10 +  self.anim_offset[0],
                                   self.pos[1] - offset[1] + self.anim_offset[1])
        else:
            animation_rect.center = (self.pos[0] - offset[0] +  self.anim_offset[0],
                                   self.pos[1] - offset[1] + self.anim_offset[1])

        surf.blit(pygame.transform.flip(animation_img, self.flip, False), animation_rect.topleft)
        self.render_health_bar(surf, offset)
        self.is_dead = self.animation.done 

class Enemy(PhysicsEntity): 
    def __init__(self, game, pos, monster_type, e_type='enemy'): 
        health_values = {'demon': 120, 'horse': 50, 'ghost': 80}
        self.monster_type = monster_type
        super().__init__(game, e_type, pos, health_values[monster_type])
        self.size = [30, 30] 
        self.walking = 0 
        self.attack_motion = 0
        self.is_damaged = False
        self.die = False
        

        if self.monster_type == 'demon':
            self.attack_sound = pygame.mixer.Sound('data/sfx/demon_attack.wav')
            self.anim_offsets = {'idle': [-20, -21], 'attack': [-60, -45], 'die': [-351, -45]}
            self.die_sound = pygame.mixer.Sound('data/sfx/demon_die.wav')
            self.die_sound.set_volume(0.7)

        elif self.monster_type == 'horse': 
            self.anim_offsets = {'idle': [-5, -16], 'run': [-5, -16], 'fall': [-5, -16], 'die': [-5, -16]}
            self.die_sound = pygame.mixer.Sound('data/sfx/horse_die.wav')
            self.die_sound.set_volume(0.55)
        elif self.monster_type == 'ghost':
            self.attack_sound = pygame.mixer.Sound('data/sfx/ghost_attack.wav')
            self.anim_offsets = {'idle': [-5, -11], 'run': [-5, -11], 'fall': [-5, -11], 'attack': [-5, -11],'die': [-5, -11]}
            self.die_sound = pygame.mixer.Sound('data/sfx/ghost_die.mp3')
            self.die_sound.set_volume(0.35)
    
    def update(self, tilemap,surf, movement=(0, 0)): 
        if self.velocity[1] >= 8: 
            self.game.enemies.remove(self)
        if self.die:
            self.set_action('die')
            self.is_damaged = False
            self.animation.update()
            if not channel6.get_busy():
                channel6.play(self.die_sound)
            return 

        if self.monster_type == 'demon': 
            self.velocity[1] = 0

        player = self.game.player
        distance_to_player = player.pos[0] + player.anim_offset[0] - self.pos[0] - self.anim_offset[0]
        same_level = abs(player.pos[1] + player.anim_offset[1] - self.pos[1] - self.anim_offset[1]) < self.size[1]

        if self.monster_type in ['demon', 'ghost'] and same_level and abs(distance_to_player) < 100 and player.dash == False:
            if distance_to_player > 0:
                movement = (0.2, movement[1])
                self.flip = False
            else:
                movement = (-0.2, movement[1])
                self.flip = True

        if self.walking and self.monster_type == 'demon':
            if not (self.collisions['left'] or self.collisions['right']):
                movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else: 
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
        elif self.walking and self.monster_type != 'demon':
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
            self.walking = random.randint(30, 120)

        monster_rect = self.rect()
        monster_rect.width += (10 if (not player.flip) and (self.monster_type == 'demon') else 5)
        monster_rect.height += 15 if self.monster_type == 'demon' else 0
        if self.action == 'attack': 
            monster_rect.center = (self.pos[0] + self.anim_offsets['idle'][0], self.pos[1] + self.anim_offsets['idle'][1])
        else: 
            monster_rect.center = (self.pos[0] + self.anim_offset[0], self.pos[1] + self.anim_offset[1])
        player_rect = player.rect()
        player_rect.center = (player.pos[0] + player.anim_offset[0] , player.pos[1] + player.anim_offset[1])
        if self.monster_type == 'demon' and not self.flip and self.action == 'attack':
            monster_rect.center = (self.pos[0] + self.anim_offset[0]+43, self.pos[1] + self.anim_offset[1]+8)

        if self.monster_type in ['demon', 'ghost']:
            if monster_rect.colliderect(player_rect):
                if not self.attack_motion:
                    self.set_action('attack')
                    self.attack_motion = 60 if self.monster_type == 'demon' else 48
                frame = self.animation.frame
                dur = self.animation.duration
    
                if int(frame/dur) == len(self.animation.images) - 1: 
                    player.health -= 2 if self.monster_type == 'demon' else 0.5
                    if  not channel7.get_busy():
                        channel7.play(player.hurt_sound)
                    if player.health <= 0: 
                        self.game.screenshake = max(12, self.game.screenshake)
            if self.attack_motion:
                self.walking = 0
                self.attack_motion -= 1
            else:
                self.set_action('idle')
        
        if self.anim_offset != self.anim_offsets[self.action]: 
            self.anim_offset = self.anim_offsets[self.action]
        if abs(player.dashes) >= 50:
            self.game.screenshake = max(12, self.game.screenshake)
            if monster_rect.colliderect(player_rect):
                self.is_damaged = True
                self.health -= 3
                if self.monster_type != 'demon':
                    movement = (movement[0], -2)
        if player.action == 'attack':
            if monster_rect.colliderect(player_rect):
                self.is_damaged = True
                self.health -= 2
        else:
            self.is_damaged = False
        if self.health <= 0: 
            self.die = True

        
        if self.is_damaged and self.monster_type != 'demon': 
            if (self.pos[0] + self.anim_offset[0] - player.pos[0] - player.anim_offset[0]) > 0:
                movement = (0.5, movement[1])
            else: 
                movement = (-0.5, movement[1])
        
        if self.action == 'attack': 
            if not channel1.get_busy():
                channel1.play(self.attack_sound)
            
        super().update(tilemap=tilemap, movement=movement)


    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.monster_type + '-' + self.action].copy()

    def render(self, surf, offset=(0, 0)):

        animation_img = self.animation.img()
        animation_rect = self.rect()
        if self.monster_type == 'demon' and not self.flip and (self.action in ['attack', 'die']):
            animation_rect.center = (self.pos[0] - offset[0] + self.anim_offset[0] + 43,
                                     self.pos[1] - offset[1] + self.anim_offset[1] + 8)
        else: 
            animation_rect.center = (self.pos[0] - offset[0] + self.anim_offset[0],
                                     self.pos[1] - offset[1] + self.anim_offset[1])
            
        if self.is_damaged:
            overlay = (255, 0, 0)
            animation_img  = add_color_overlay(animation_img, overlay, 128)  

        surf.blit(pygame.transform.flip(animation_img, self.flip, False), animation_rect.topleft)
        if not self.die: self.render_health_bar(surf, offset)
        if self.animation.done: 
            self.game.enemies.remove(self)
            



channel0 = pygame.mixer.Channel(0)
channel1 = pygame.mixer.Channel(1)
channel2 = pygame.mixer.Channel(2)
channel3 = pygame.mixer.Channel(3)
channel4 = pygame.mixer.Channel(4)
channel5 = pygame.mixer.Channel(5)
channel6 = pygame.mixer.Channel(6)
channel7 = pygame.mixer.Channel(7)
