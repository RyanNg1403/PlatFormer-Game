import pygame
import math
import random
import sys
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
from scripts.particles import Particle
pygame.mixer.pre_init(44100, -16, 512)  
class Game:
    def __init__(self): 
        pygame.init()
        pygame.display.set_caption('Godthic Adventure') # Set the name for the application
        # Create a screen/window    
        self.screen = pygame.display.set_mode((960,720))
        # The display is half the size of the screen and used to scale the image
        self.display = pygame.Surface((320, 240))
        # Creat a variable for time w
        self.clock = pygame.time.Clock()
        self.assets = {
            'grass' : load_images('tiles/grass', overlay=True),
            'large_decor' : load_images('tiles/large_decor', overlay=True),
            'stone' : load_images('tiles/stone', overlay=True),
            'decor' : load_images('tiles/decor'),
            'background': pygame.transform.scale(load_image('background2.png'), (320, 240)),
            'clouds': load_images('clouds'),
            'enemy/demon-idle': Animation(load_images('enemy/demon-idle', scale=2, flip=True), img_duration=6),
            'enemy/demon-run': Animation(load_images('enemy/demon-idle', scale=2,flip=True), img_duration=6),
            'enemy/demon-fall': Animation(load_images('enemy/demon-idle', scale=2, flip=True), img_duration=6),
            'enemy/demon-attack': Animation(load_images('enemy/demon-attack2', scale=1.1, flip=True), img_duration=6),
            'enemy/demon-die': Animation(load_images('enemy/demon-die', scale=1.7, flip=True), img_duration=3,loop=False),
            'enemy/horse-idle': Animation(load_images('enemy/horse-idle', scale=2, flip=True), img_duration=6),
            'enemy/horse-attack': Animation(load_images('enemy/horse-idle', scale=2, flip=True), img_duration=6),
            'enemy/horse-run': Animation(load_images('enemy/horse-run', scale=2, flip=True), img_duration=6),
            'enemy/horse-die': Animation(load_images('enemy/horse-idle', scale=2, flip=True), img_duration=6,loop=False),
            'enemy/horse-fall': Animation(load_images('enemy/horse-idle', scale=2, flip=True), img_duration=6),
            'enemy/ghost-idle': Animation(load_images('enemy/ghost-idle', scale=1.5, flip=True), img_duration=6),
            'enemy/ghost-run': Animation(load_images('enemy/ghost-idle', scale=1.5, flip=True), img_duration=6),
            'enemy/ghost-die': Animation(load_images('enemy/ghost-vanish', scale=1.5, flip=True), img_duration=6,loop=False),
            'enemy/ghost-fall': Animation(load_images('enemy/ghost-idle', scale=1.5, flip=True), img_duration=6),
            'enemy/ghost-attack': Animation(load_images('enemy/ghost-attack', scale=1.5, flip=True), img_duration=6),
            'player/idle': Animation(load_images('final form/idle', scale=1.2), img_duration=6),
            'player/run': Animation(load_images('final form/run', scale=1.2), img_duration=4),
            'player/jump': Animation(load_images('final form/jump', scale=1.2), img_duration=15),
            'player/fall': Animation(load_images('final form/jump', scale=1.2), img_duration=5),
            'player/slide': Animation(load_images('final form/crouch-slash', scale=1.2), img_duration=1),
            'player/crouch': Animation(load_images('final form/crouch', scale=1.2), img_duration=8),
            'player/attack': Animation(load_images('final form/attack', scale=1.2), img_duration=8),
            'monsters' : load_images('monsters'),
            'particle/leaf': Animation(load_images('particles/leaf', color=(105,123,140), overlay=True), img_duration=20, loop=False), 
            'spawners' : load_images('tiles/spawners'),
        }
        self.clouds = Clouds(self.assets['clouds'])
        self.img_pos = [100, 200]
        self.movement = [False, False]
        
        self.player = Player(self,(50,50))
        self.tilemap = TileMap(self)
        self.scroll = [0,0]
        self.leaf_spawners = []
        self.particles = []
        

        try:
            self.tilemap.load('tutorial.json')
        except FileNotFoundError:
            print('Map file not found')
            
        for tree in self.tilemap.extract([('large_decor', 2)]): 
            self.leaf_spawners.append(pygame.Rect(tree['pos'][0] + 4, 
                                                  tree['pos'][1] + 4,
                                                  23,13))
        self.enemies = []
        for monster in self.tilemap.extract([('monsters', 0), ('monsters', 1), ('monsters',2)], keep=True): 
            if monster['variant'] == 0: 
                self.enemies.append(Enemy(self, monster['pos'], monster_type = 'demon'))
            if monster['variant'] == 1: 
                self.enemies.append(Enemy(self, monster['pos'], monster_type = 'ghost'))
            if monster['variant'] == 2: 
                self.enemies.append(Enemy(self, monster['pos'], monster_type = 'horse'))
        pygame.mixer.music.load('data/sfx/background_lv1.mp3') 
        pygame.mixer.music.set_volume(0.5) 
        pygame.mixer.music.play(-1)
    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0,0))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width()//2 - self.scroll[0]) // 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height()//2 - self.scroll[1]) // 10
            
            for leaf_rect in self.leaf_spawners:
                if random.random() * 46969  < leaf_rect.width * leaf_rect.height:
                    pos = (leaf_rect.x + random.random()* leaf_rect.width, leaf_rect.y + random.random()* leaf_rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, [-0.1,0.3], random.randint(0,20)))
            
            self.clouds.update()
            self.clouds.render(self.display, offset= self.scroll)
            self.tilemap.render(self.display, offset = self.scroll)
            for enemy in self.enemies.copy(): 
                enemy.update(self.tilemap, (0,0))
                enemy.render(self.display, offset = self.scroll)
                
            self.player.update(self.tilemap, (self.movement[1]- self.movement[0], 0))
            self.player.render(self.display, offset = self.scroll)
            


            for particle in self.particles.copy(): 
                kill = particle.update()
                particle.render(self.display, self.scroll)
                if particle.type == 'leaf': 
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:  
                    self.particles.remove(particle)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT: # Meaning that you clicked the X button on the screen
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                         self.movement[1] = True
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_k:
                        self.player.dash()
                    if event.key == pygame.K_s:
                        self.player.crouching = True
                    if event.key == pygame.K_l: 
                        self.player.attack = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_s:
                        self.player.crouching = False
                    if event.key == pygame.K_l: 
                        self.player.attack = False
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0,0))
            pygame.display.update() 
            self.clock.tick(60)   # 60 FPS

Game().run()