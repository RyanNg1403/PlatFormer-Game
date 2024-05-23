import pygame
import math
import random
import sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
from scripts.particles import Particle
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Nigga Hunter') # Set the name for the application
        # Create a screen/window
        self.screen = pygame.display.set_mode((640,480))
        # The display is half the size of the screen and used to scale the image
        self.display = pygame.Surface((320, 240))
        # Creat a variable for time 
        self.clock = pygame.time.Clock()
        
        self.assets = {
            'player' : load_image('entities/player.png'), 
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'decor' : load_images('tiles/decor'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_duration=6),
            'player/run': Animation(load_images('entities/player/run'), img_duration=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_duration=5),
            'player/slide': Animation(load_images('entities/player/slide'), img_duration=5),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_duration=5),
            'spawners' : load_images('tiles/spawners'),
            'particle/leaf': Animation(load_images('particles/leaf'), img_duration=20, loop=False)
        }
        self.clouds = Clouds(self.assets['clouds'])
        self.img_pos = [100, 200]
        self.movement = [False, False]
        self.player = Player(self,(50,50), (8,12))
        self.tilemap = TileMap(self)
        self.scroll = [0,0]
        self.leaf_spawners = []
        self.particles = []
        
            

        try:
            self.tilemap.load('tutorial.json')
        except FileNotFoundError:
            print('Map file not found!, BIATCH')
            
        for tree in self.tilemap.extract([('large_decor', 2)]): 
            print(tree)
            self.leaf_spawners.append(pygame.Rect(tree['pos'][0] + 4, 
                                                  tree['pos'][1] + 4,
                                                  23,13))
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
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0,0))
            pygame.display.update() 
            self.clock.tick(60)   # 60 FPS

Game().run()