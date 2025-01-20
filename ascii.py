import time
import cv2
import numpy as np
import keyboard
import random
import os
# Character set
#c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
#c = ' .`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
c = ' .:-=+*#%@'
#c = '@#%+=-:. '



# Desired output dimensions (width and height of ASCII art in characters)
#max_width = 100
#max_height = 100

#c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#$%&()*+,-./:;<=>?@[\]^_`{|}~                                  '


# Create a function to map grayscale values to characters
def map_to_char(value, scale_factor):
    index = int(value / scale_factor)  # Scale the value to the character set
    return c[index]


"""
for i, row in enumerate(chartable):
    for j, char in enumerate(row):
        chartable[i][j] = random.choice(c)

def print_table(chartable):
    for row in chartable:
        for char in row:
            print(char, end=' ')
        print()
        
def populate_table_randomly(charset, width, height):
    c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#$%&()*+,-./:;<=>?@[\]^_`{|}~                                  '
    chartable = [['x' for _ in range(width)] for _ in range(height)]
    for i, row in enumerate(chartable):
        for j, char in enumerate(row):
            chartable[i][j] = random.choice(c)
            return chartable

def populate_table_from_set(chartable):
    for i, row in reversed(list(enumerate(chartable))):
        for j, char in enumerate(row):
            if i > 0:
                chartable[i][j] = chartable[i-1][j]
            else:
                chartable[i][j] = random.choice(c)
    return chartable"""



def print_table(chartable):
    for row in chartable:
        for char in row:
            print(char, end='')
        print()
        


def image_to_ascii(image_scale_factor = 0.1):
    # Read the image and convert it to grayscale
    image = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)
    #image = cv2.imread('test2.jpg', cv2.IMREAD_GRAYSCALE)
    print("original shape:", image.shape)


    # Calculate the new height to maintain aspect ratio
    original_height, original_width = image.shape
    image_aspect_ratio = original_height / original_width  # Image aspect ratio (height/width)
    print("Image aspect ratio:", image_aspect_ratio)
    character_aspect_ratio = 2  # Approximate height-to-width ratio of characters
    adjusted_height = int((image_scale_factor*original_height)/character_aspect_ratio)
    adjusted_width = int(image_scale_factor*original_width)
    
    # Resize the image
    resized_image = cv2.resize(image, (adjusted_width, adjusted_height), interpolation=cv2.INTER_AREA)

    # Calculate the mapping factor
    num_chars = len(c)
    scale_factor = 255 / (num_chars - 1)
    
    # Replace each pixel with the corresponding character
    height, width = resized_image.shape
    original_char_image = np.array([[map_to_char(resized_image[y, x], scale_factor) for x in range(width)] for y in range(height)])
    return original_char_image


image_scale_factor = 0.1
original_char_image = image_to_ascii(image_scale_factor)
char_image = np.copy(original_char_image)
max_chance = 0.1
weights = [max_chance / (i + 1) for i in range(original_char_image.shape[0])]
#weights.reverse()

print(original_char_image.shape)
print(weights)
time.sleep(2)



while True:
    #print(keyboard.read_key())
    """
    if keyboard.is_pressed('+'):
        print("increasing image scale factor")
        image_scale_factor += 0.05
    if keyboard.is_pressed('-'):
        print("decreasing image scale factor")
        image_scale_factor -= 0.05
    if image_scale_factor < 0.05:
        image_scale_factor = 0.05
    """ 
    
        
    
    
    """
    #print(char_image)
    
    #--------------------
    # IMAGE SCROLLING DOWN REPEATEDLY
    while True:
        for i, row in reversed(list(enumerate(char_image))):
            for j, char in enumerate(row):
                if i > 0:
                    char_image[i][j] = char_image[i-1][j]
                else:
                    char_image[i][j] = char_image[i-1][j]
        os.system('cls' if os.name == 'nt' else 'clear')
        print_table(char_image)
        time.sleep(0.05)
    """
    
    #pour_symbol = random.choice("|*xoO1")
    pour_symbol = random.choice("|")
    
    for i, row in reversed(list(enumerate(char_image))):
        for j, char in enumerate(row):
            #print(i,j)
            #the chance of droplets is increased the closer we are to the top
            #print(i, j)
            #print(random.random(), weights[i])
            #i : 37...0
            #[0.9 ... 0]
            if weights[i]/100 > random.random():
                char_image[i][j] = pour_symbol
                pour_length = random.randint(1,3)
                if i > pour_length:
                    for cell in range(pour_length):
                        char_image[cell][j] = pour_symbol
            
            if weights[i]+0.3 > random.random():
                if i != 0:
                    if char_image[i-1][j]  == pour_symbol:
                        char_image[i][j] = pour_symbol
            
            if i  > random.randint(0,100):
                char_image[i][j] = original_char_image[i][j]
        
    os.system('cls' if os.name == 'nt' else 'clear')
        
        
    poured_ascii_art = "\n".join("".join(row) for row in char_image)
    print(poured_ascii_art)
    
    original_ascii_art = "\n".join("".join(row) for row in original_char_image)
    print(original_ascii_art)
    #30fps
    time.sleep(0.02)
    
    """
    while True:
        for i, row in reversed(list(enumerate(char_image))):
            for j, char in enumerate(row):
                if char == " ":
                    if char[i+1][j] == " ":
                        continue
                    elif 
    """
                        
    
    

