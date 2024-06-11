import pygame

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
import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Game with Text Outline')
        self.screen = pygame.display.set_mode((960, 720))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 72)  # Choose a font and size
        self.text_color = (255, 255, 255)  # White text color
        self.outline_color = (0, 0, 0)  # Black outline color
        self.outline_thickness = 2  # Thickness of the outline

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((50, 50, 50))  # Fill the screen with a background color

            text_surface = render_text_with_outline(
                "Outlined Text",
                self.font,
                self.text_color,
                self.outline_color,
                self.outline_thickness
            )

            # Center the text on the screen
            text_rect = text_surface.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(text_surface, text_rect.topleft)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
