import os
import pygame

def get_image_sizes(directory):
    # Initialize Pygame
    pygame.init()

    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # List all files in the directory
    files = os.listdir(directory)

    # Filter out only image files (assuming common image file extensions)
    image_files = [file for file in files if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]

    # Dictionary to store image sizes
    image_sizes = {}

    # Load each image and get its size
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        try:
            image = pygame.image.load(image_path)
            image_sizes[image_file] = image.get_size()
        except pygame.error as e:
            print(f"Failed to load image '{image_file}': {e}")

    # Quit Pygame
    pygame.quit()

    return image_sizes

def main():
    # Replace 'your_directory_path' with the path to your directory containing images
    directory = "C:/Users/PhatNguyen/OneDrive/Desktop/OOP/data/images/final form/jump"

    # Get image sizes
    sizes = get_image_sizes(directory)

    # Print the sizes of the images
    if sizes:
        for image_file, size in sizes.items():
            print(f"Image: {image_file}, Size: {size}")

if __name__ == "__main__":
    main()
