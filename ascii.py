import time
import cv2
import numpy as np
import keyboard

# Character set
#c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
#c = ' .`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
c = ' .:-=+*#%@'
#c = '@#%+=-:. '



# Desired output dimensions (width and height of ASCII art in characters)
#max_width = 100
#max_height = 100


# Read the image and convert it to grayscale
image = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)
#image = cv2.imread('test2.jpg', cv2.IMREAD_GRAYSCALE)
print("original shape:", image.shape)


# Calculate the new height to maintain aspect ratio
original_height, original_width = image.shape
image_aspect_ratio = original_height / original_width  # Image aspect ratio (height/width)
image_scale_factor = 0.1
print("Image aspect ratio:", image_aspect_ratio)
character_aspect_ratio = 2  # Approximate height-to-width ratio of characters




# Create a function to map grayscale values to characters
def map_to_char(value):
    index = int(value / scale_factor)  # Scale the value to the character set
    return c[index]


while True:
    #print(keyboard.read_key())
    
    if keyboard.is_pressed('+'):
        print("increasing image scale factor")
        image_scale_factor += 0.05
    if keyboard.is_pressed('-'):
        print("decreasing image scale factor")
        image_scale_factor -= 0.05
    if image_scale_factor < 0.05:
        image_scale_factor = 0.05
        
    print(image_scale_factor)
    
    adjusted_height = int((image_scale_factor*original_height)/character_aspect_ratio)
    adjusted_width = int(image_scale_factor*original_width)
    
    # Resize the image
    resized_image = cv2.resize(image, (adjusted_width, adjusted_height), interpolation=cv2.INTER_AREA)

    # Calculate the mapping factor
    num_chars = len(c)
    scale_factor = 255 / (num_chars - 1)
    
    # Replace each pixel with the corresponding character
    height, width = resized_image.shape
    char_image = np.array([[map_to_char(resized_image[y, x]) for x in range(width)] for y in range(height)])
    print("ascii shape", char_image.shape)

    # Combine the characters into lines to visualize as text
    ascii_art = "\n".join("".join(row) for row in char_image)
    
    # Print the ASCII art
    print(ascii_art)
    time.sleep(0.5)
