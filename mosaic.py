from PIL import Image
import numpy as np
import os

# Function to load images from a directory
def load_images(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"): # Change extensions as needed
            img = Image.open(os.path.join(directory, filename))
            images.append(img)
    return images

# Function to resize images to a specified size
def resize_images(images, size):
    resized_images = []
    for img in images:
        resized_img = img.resize(size, Image.ANTIALIAS)
        resized_images.append(resized_img)
    return resized_images

# Function to create a mosaic image
def create_mosaic(images, rows, cols):
    # Calculate tile size
    tile_width = images[0].width
    tile_height = images[0].height

    # Create a blank canvas for the mosaic
    mosaic_width = tile_width * cols
    mosaic_height = tile_height * rows
    mosaic = Image.new('RGB', (mosaic_width, mosaic_height))

    # Paste images onto the canvas
    for i in range(rows):
        for j in range(cols):
            index = i * cols + j
            if index < len(images):
                mosaic.paste(images[index], (j * tile_width, i * tile_height))

    return mosaic

# Main function
def main():
    # Specify directory containing tile images
    tile_directory = "tiles"

    # Load tile images
    tile_images = load_images(tile_directory)

    # Resize tile images to a consistent size (e.g., 50x50 pixels)
    resized_tile_images = resize_images(tile_images, (50, 50))

    # Specify the number of rows and columns for the mosaic
    rows = 10
    cols = 10

    # Create the mosaic image
    mosaic = create_mosaic(resized_tile_images, rows, cols)

    # Save the mosaic image
    mosaic.save("mosaic_image.jpg")

if __name__ == "__main__":
    main()
