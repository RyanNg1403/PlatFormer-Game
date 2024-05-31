import pygame
import sys
from scripts.utils import  load_images
from scripts.tilemap import TileMap

RENDER_OFFSET = 3
class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Editor') # Set the name for the application
        # Create a screen/window
        self.screen = pygame.display.set_mode((960,720))
        # The display is half the size of the screen and used to scale the image
        self.display = pygame.Surface((320, 240))
        # Creat a variable for time 
        self.clock = pygame.time.Clock()
        self.assets = {
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'decor' : load_images('tiles/decor'),
            'spawners' : load_images('tiles/spawners'),
            'monsters' : load_images('monsters', scale=2)
        }
    

        self.movement = [False, False, False, False]
        self.tilemap = TileMap(self)
        self.scroll = [0,0]
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.variant = 0
        self.left_clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        try:
            self.tilemap.load('tutorial.json')
        except FileNotFoundError:
            print('Map file not found!, BIATCH')
    def run(self):
        while True:
            
            self.display.fill((135, 206, 235))
    

            self.scroll[0] += (self.movement[1]- self.movement[0]) * 2
            self.scroll[1] += (self.movement[3]- self.movement[2]) * 2
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.variant].copy()
            current_tile_img.set_alpha(200)
            self.display.blit(current_tile_img, (5,5))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, render_scroll)
            
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0]/ RENDER_OFFSET, mpos[1] / RENDER_OFFSET)

            tile_pos = (int(mpos[0] + self.scroll[0]) // self.tilemap.tile_size, 
                        int(mpos[1] + self.scroll[1])  // self.tilemap.tile_size)
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                      tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else: 
                self.display.blit(current_tile_img, mpos)
            if self.left_clicking and self.ongrid:
                loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                self.tilemap.tilemap[loc] = {'type': self.tile_list[self.tile_group], 'variant': self.variant, 'pos': tile_pos}
                
            if self.right_clicking:
                loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if loc in self.tilemap.tilemap.keys():
                    del self.tilemap.tilemap[loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0] - self.scroll[0],tile['pos'][1]- self.scroll[1], 
                                            tile_img.get_width(), tile_img.get_height())
                    if tile_rect.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)
                    
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT: # Meaning that you clicked the X button on the screen
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.left_clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.variant, 
                                                               'pos': (mpos[0] + self.scroll[0] , mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if not self.shift:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list) 
                            self.variant = 0  
                    else:
                        if event.button == 4:
                            self.variant = (self.variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.variant = (self.variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('tutorial.json')
                        print('Saved Successfully!')
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0,0))
            pygame.display.update() 
            self.clock.tick(60)   # 60 FPS

Editor().run()