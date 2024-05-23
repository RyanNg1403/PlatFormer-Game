import os 
import pygame

BASE_IMG_PATH = 'data/images/'
def load_image(path):
    '''
    Load a image'''
    img = pygame.image.load(BASE_IMG_PATH + path).convert() # .convert to make it run faster
    img.set_colorkey((0,0,0))
    return  img

def load_images(path):
    '''
    Load several images'''
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images
class Animation:
    def __init__(self, images, img_duration=5, loop=True):
        self.images =list(images) # All the imgs of an action
        self.duration = img_duration # The num of iterations for each img
        self.loop = loop # Loop through all the imgs 
        self.done = False # is True when Loop is False and is out of imgs
        self.frame = 0
    def update(self):   
        if self.loop:
            self.frame = (self.frame +1) % (self.duration * len(self.images))
        else:
            self.frame = min(self.frame+1, self.duration * self.len(self.images) - 1)
            if self.frame >= self.duration * len(self.images) - 1:
                self.done = True
    def img(self):
        # Return the img at a particular frame
        return self.images[int(self.frame / self.duration)]
    def copy(self):
        return Animation(self.images, self.duration, self.loop)
    
        