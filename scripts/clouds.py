import pygame
import random
class Cloud:
    def __init__(self, img, pos, speed, depth):
        self.pos = pos
        self.pos = list(pos)
        self.speed = speed
        self.img = img
        self.depth = depth
    
    def update(self):
        self.pos[0] += self.speed
    def render(self, surf, offset):
        render_pos = [self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth]
        render_pos[0] = render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width()
        render_pos[1] = render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()
        surf.blit(self.img, render_pos)
        
class Clouds:
    def __init__(self, cloud_imgs, count = 16):
        self.clouds = []

        for i in range(count):
            pos = (random.random() * 9999, random.random() * 9999)
            speed = random.random() * 0.05 + 0.05
            depth = random.random() * 0.6 + 0.2
            self.clouds.append(Cloud(random.choice(cloud_imgs), pos, speed, depth))
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()
    def render(self, surf, offset):
         for cloud in self.clouds:
             cloud.render(surf, offset) 

        