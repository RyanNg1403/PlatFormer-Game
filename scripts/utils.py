import os 
import pygame

BASE_IMG_PATH = 'data/images/'
def load_image(path,overlay= False, scale = 1, flip = False, color = (17, 56, 107)):
    '''
    Load a image'''
    img = pygame.image.load(BASE_IMG_PATH + path)# .convert to make it run faster
    img.set_colorkey((0,0,0))
    size = img.get_size()
    if flip: 
        img = pygame.transform.flip(img, True, False)
    img = pygame.transform.scale(img, (size[0]//scale, size[1]//scale))
    if overlay: 
        img = add_color_overlay(img,color , 128)
    return  img

def load_images(path, overlay = False, scale = 1, flip = False, color = (17, 56, 107)):
    '''
    Load several images'''
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name, overlay, scale, flip, color))
    return images


def add_color_overlay(image, color, alpha):
    """
    Add a color overlay to an image in Pygame.

    :param image: The original Pygame surface (image).
    :param color: The color to overlay (RGB tuple).
    :param alpha: The alpha transparency of the overlay (0 to 255).
    :return: A new Pygame surface with the color overlay.
    """
    # Create a copy of the image to avoid modifying the original
    overlay_image = image.copy()
    
    # Create a transparent surface with the same dimensions as the image
    overlay = pygame.Surface(overlay_image.get_size(), pygame.SRCALPHA)
    
    # Fill the overlay with the specified color and alpha transparency
    overlay.fill((*color, alpha))
    
    # Blit the overlay onto the image
    overlay_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    return overlay_image

def render_text_with_outline(text, font, text_color, outline_color, outline_thickness):
    # Render the outline text
    outline_image = font.render(text, True, outline_color)
    text_image = font.render(text, True, text_color)

    # Create a new surface to hold both text and outline
    width = text_image.get_width() + 2 * outline_thickness
    height = text_image.get_height() + 2 * outline_thickness
    combined_image = pygame.Surface((width, height), pygame.SRCALPHA)

    # Blit the outline text at multiple positions to create the outline effect
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0:  # Skip the center position
                combined_image.blit(outline_image, (dx + outline_thickness, dy + outline_thickness))

    # Blit the main text in the center
    combined_image.blit(text_image, (outline_thickness, outline_thickness))

    return combined_image

class Animation:
    def __init__(self, images, img_duration=5, loop=True, SpriteSheet = False):
        if not SpriteSheet:
            self.images =list(images)

        self.duration = img_duration # The num of iterations for each img
        self.loop = loop # Loop through all the imgs 
        self.done = False # is True when Loop is False and is out of imgs
        self.frame = 0
    def update(self):   
        if self.loop:
            self.frame = (self.frame +1) % (self.duration * len(self.images))
        else:
            self.frame = min(self.frame+1, self.duration * len(self.images) - 1)
            if self.frame >= self.duration * len(self.images) - 1:
                self.done = True
    def img(self):
        # Return the img at a particular frame
        return self.images[int(self.frame / self.duration)].convert_alpha()
    def copy(self):
        return Animation(self.images, self.duration, self.loop)