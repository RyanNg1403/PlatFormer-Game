import pygame
import math
import random
import sys
from scripts.entities import  Player, Enemy
from scripts.utils import  load_images, Animation, render_text_with_outline
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
from scripts.particles import Particle

pygame.mixer.pre_init(44100, -16, 512)

class Menu:
    def __init__(self, button_images, font_path, game):
        self.buttons = {
            'play': button_images[0],
            'settings': button_images[1],
            'exit': button_images[2],
        }
        self.font = pygame.font.Font(font_path, 55)  # Load custom font
        self.title_text = render_text_with_outline(
                "Godthic Adventure",
                self.font,
                (143, 1, 18),
                (46, 16, 28),
                3
            )
        self.game = game
    def draw(self, screen):
        menu_img = pygame.transform.scale(self.game.assets['background'][3], screen.get_size())
        screen.blit(menu_img, (0,0))
        screen.blit(self.title_text, (screen.get_width()//2 - self.title_text.get_width()//2, 100))

        y = 300
        for key, button in self.buttons.items():
            screen.blit(button, (screen.get_width()//2 - button.get_width()//2, y))
            y += 100

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.buttons['play'].get_rect(topleft=(480 - self.buttons['play'].get_width()//2, 300)).collidepoint(mouse_x, mouse_y):
                return 'play'
            elif self.buttons['exit'].get_rect(topleft=(480 - self.buttons['exit'].get_width()//2, 500)).collidepoint(mouse_x, mouse_y):
                return 'exit'
        return None


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Godthic Adventure')
        self.screen = pygame.display.set_mode((960, 720))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.assets = {
            'grass': load_images('tiles/grass', overlay=True),
            'large_decor': load_images('tiles/large_decor', overlay=True),
            'stone': load_images('tiles/stone', overlay=True),
            'decor': load_images('tiles/decor'),
            'background': load_images('background'),
            'clouds': load_images('clouds'),
            'enemy/demon-idle': Animation(load_images('enemy/demon-idle', scale=2, flip=True), img_duration=6),
            'enemy/demon-run': Animation(load_images('enemy/demon-idle', scale=2, flip=True), img_duration=6),
            'enemy/demon-fall': Animation(load_images('enemy/demon-idle', scale=2, flip=True), img_duration=6),
            'enemy/demon-attack': Animation(load_images('enemy/demon-attack2', scale=1.1, flip=True), img_duration=6),
            'enemy/demon-die': Animation(load_images('enemy/demon-die', scale=1.7, flip=True), img_duration=3, loop=False),
            'enemy/horse-idle': Animation(load_images('enemy/horse-idle', scale=2, flip=True), img_duration=6),
            'enemy/horse-attack': Animation(load_images('enemy/horse-idle', scale=2, flip=True), img_duration=6),
            'enemy/horse-run': Animation(load_images('enemy/horse-run', scale=2, flip=True), img_duration=6),
            'enemy/horse-die': Animation(load_images('enemy/horse-idle', scale=2, flip=True), img_duration=6, loop=False),
            'enemy/horse-fall': Animation(load_images('enemy/horse-idle', scale=2, flip=True), img_duration=6),
            'enemy/ghost-idle': Animation(load_images('enemy/ghost-idle', scale=1.5, flip=True), img_duration=6),
            'enemy/ghost-run': Animation(load_images('enemy/ghost-idle', scale=1.5, flip=True), img_duration=6),
            'enemy/ghost-die': Animation(load_images('enemy/ghost-vanish', scale=1.5, flip=True), img_duration=6, loop=False),
            'enemy/ghost-fall': Animation(load_images('enemy/ghost-idle', scale=1.5, flip=True), img_duration=6),
            'enemy/ghost-attack': Animation(load_images('enemy/ghost-attack', scale=1.5, flip=True), img_duration=6),
            'player/idle': Animation(load_images('final form/idle', scale=1.2), img_duration=6),
            'player/run': Animation(load_images('final form/run', scale=1.2), img_duration=4),
            'player/jump': Animation(load_images('final form/jump', scale=1.2), img_duration=15),
            'player/fall': Animation(load_images('final form/jump', scale=1.2), img_duration=5),
            'player/slide': Animation(load_images('final form/crouch-slash', scale=1.2), img_duration=1),
            'player/crouch': Animation(load_images('final form/crouch', scale=1.2), img_duration=8),
            'player/attack': Animation(load_images('final form/attack', scale=1.2), img_duration=8),
            'player/die': Animation(load_images('final form/hurt', scale=1.2), img_duration=8, loop=False),
            'monsters': load_images('monsters'),
            'particle/leaf': Animation(load_images('particles/leaf', color=(105, 123, 140), overlay=True), img_duration=20, loop=False),
            'spawners': load_images('tiles/spawners'),
            'buttons': load_images('menu', scale=2)
        }
        self.clouds = Clouds(self.assets['clouds'])
        self.img_pos = [100, 200]
        self.movement = [False, False]

        self.player = Player(self, (50, 50))
        self.tilemap = TileMap(self)
        self.game_over = False
        self.scroll = [0, 0]
        self.leaf_spawners = []
        self.particles = []
        self.level = 0
        self.dead = 0
        self.screenshake = 0
        self.enemies = []
        self.transition = -30
        font_path = 'data/font/font3.TTF'  # Set the path to your font file
        self.menu = Menu(self.assets['buttons'], font_path, self)
        self.in_menu = True

        try:
            self.tilemap.load('data/maps/' +str(self.level) + '.json')
        except FileNotFoundError:
            print('Map file not found')

        for tree in self.tilemap.extract([('large_decor', 2)]):
            self.leaf_spawners.append(pygame.Rect(tree['pos'][0] + 4,
                                                  tree['pos'][1] + 4,
                                                  23, 13))

        for monster in self.tilemap.extract([('monsters', 0), ('monsters', 1), ('monsters', 2)], keep=True):
            if monster['variant'] == 0:
                self.enemies.append(Enemy(self, monster['pos'], monster_type='demon'))
            if monster['variant'] == 1:
                self.enemies.append(Enemy(self, monster['pos'], monster_type='ghost'))
            if monster['variant'] == 2:
                self.enemies.append(Enemy(self, monster['pos'], monster_type='horse'))
        pygame.mixer.music.load('data/sfx/background_lv1.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        self.leaf_spawners = []
        self.enemies = []
        self.player = Player(self, (50, 50))
        self.player.air_time = 0
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        for monster in self.tilemap.extract([('monsters', 0), ('monsters', 1), ('monsters', 2)], keep=True):
            if monster['variant'] == 0:
                self.enemies.append(Enemy(self, monster['pos'], monster_type='demon'))
            if monster['variant'] == 1:
                self.enemies.append(Enemy(self, monster['pos'], monster_type='ghost'))
            if monster['variant'] == 2:
                self.enemies.append(Enemy(self, monster['pos'], monster_type='horse'))
        self.dead = 0
        self.scroll = [0, 0]
        self.particles = []
        self.transition = -30

    def run(self):
        while True:
            self.screenshake = max(0, self.screenshake - 1)

            if self.in_menu:
                self.menu.draw(self.screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    action = self.menu.handle_event(event)
                    if action == 'play':
                        self.in_menu = False
                    elif action == 'exit':
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                self.clock.tick(60)
                continue

            if not self.enemies:
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, 2)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 30:
                    self.transition = min(30, self.transition + 1)
                if self.dead == 60:
                    self.load_level(self.level)
            if self.player.velocity[1] >= 10:
                self.load_level(self.level)
            self.display.blit(pygame.transform.scale(self.assets['background'][self.level], (320, 240)), (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() // 2 - self.scroll[0]) // 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() // 2 - self.scroll[1]) // 10

            for leaf_rect in self.leaf_spawners:
                if random.random() * 46969 < leaf_rect.width * leaf_rect.height:
                    pos = (leaf_rect.x + random.random() * leaf_rect.width, leaf_rect.y + random.random() * leaf_rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, [-0.1, 0.3], random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display, offset=self.scroll)
            self.tilemap.render(self.display, offset=self.scroll)
            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, self.display, (0, 0))
                enemy.render(self.display, offset=self.scroll)
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=self.scroll)
                if self.player.is_dead:
                    self.dead += 1

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, self.scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)

Game().run()
