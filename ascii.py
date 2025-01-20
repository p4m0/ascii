import time
import cv2
import numpy as np
import keyboard
import random
import os
import math
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
        


def image_to_ascii(path_to_image, image_scale_factor = 0.1):
    # Read the image and convert it to grayscale
    image = cv2.imread(path_to_image, cv2.IMREAD_GRAYSCALE)
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
    original_ascii = np.array([[map_to_char(resized_image[y, x], scale_factor) for x in range(width)] for y in range(height)])
    return original_ascii

image_scale_factor = 0.1
original_ascii = image_to_ascii("test.png", image_scale_factor)
modified_ascii = np.copy(original_ascii)
max_chance = 0.1
weights = [max_chance / (i + 1) for i in range(original_ascii.shape[0])]
#weights.reverse()

print(len(original_ascii))
print(weights)
print(type(modified_ascii))
time.sleep(2)

def pour_effect(ascii_array, empty_char=' '):
    """Simulate pouring effect by making characters fall down."""
    modified_ascii = [list(row) for row in ascii_array]
    for i, row in reversed(list(enumerate(modified_ascii))):
        for j, char in enumerate(row):
            if char != empty_char and i < len(modified_ascii) - 1:
                if modified_ascii[i + 1][j] == empty_char:
                    modified_ascii[i + 1][j], modified_ascii[i][j] = char, empty_char
    return np.array(modified_ascii)

def drip_effect(ascii_array, empty_char=' '):
    """Simulate dripping effect by randomly making characters fall down."""
    modified_ascii = [list(row) for row in ascii_array]
    for i in reversed(range(len(modified_ascii) - 1)):
        for j in range(len(modified_ascii[i])):
            if modified_ascii[i][j] != empty_char and modified_ascii[i + 1][j] == empty_char:
                if random.random() < 0.5:  # 50% chance to drip down
                    modified_ascii[i + 1][j], modified_ascii[i][j] = modified_ascii[i][j], empty_char
    return np.array(modified_ascii)

def wave_effect(ascii_array, amplitude=2, frequency=0.2):
    """Simulate wave effect by shifting characters in a sine wave pattern."""
    modified_ascii = [list(row) for row in ascii_array]
    for i, row in enumerate(modified_ascii):
        shift = int(amplitude * math.sin(frequency * i))
        modified_ascii[i] = row[-shift:] + row[:-shift] if shift else row
    return np.array(modified_ascii)

def shake_effect(ascii_array):
    """Simulate shaking effect by shifting characters left or right randomly."""
    modified_ascii = [list(row) for row in ascii_array]
    for i in range(len(modified_ascii)):
        if random.random() < 0.3:  # 30% chance to shake this row
            shift = random.choice([-1, 1])
            modified_ascii[i] = modified_ascii[i][shift:] + modified_ascii[i][:shift]
    return np.array(modified_ascii)

def swirl_effect(ascii_array):
    """Simulate swirl effect by rotating characters around the center."""
    modified_ascii = [list(row) for row in ascii_array]
    center_x, center_y = len(modified_ascii) // 2, len(modified_ascii[0]) // 2
    
    for i in range(len(modified_ascii)):
        for j in range(len(modified_ascii[i])):
            dx, dy = j - center_y, i - center_x
            new_x = center_x + dy
            new_y = center_y - dx
            if 0 <= new_x < len(modified_ascii) and 0 <= new_y < len(modified_ascii[0]):
                modified_ascii[i][j], modified_ascii[new_x][new_y] = modified_ascii[new_x][new_y], modified_ascii[i][j]

    return np.array(modified_ascii)

def erosion_effect(ascii_array, empty_char=' '):
    """Gradually erodes the ASCII art by replacing random characters with spaces."""
    modified_ascii = [list(row) for row in ascii_array]
    for i in range(len(modified_ascii)):
        for j in range(len(modified_ascii[i])):
            if modified_ascii[i][j] != empty_char and random.random() < 0.1:
                modified_ascii[i][j] = empty_char
    return np.array(modified_ascii)

def wind_effect(ascii_array, empty_char=' '):
    """Simulate wind effect by moving characters to the right."""
    modified_ascii = [list(row) for row in ascii_array]
    for i in range(len(modified_ascii)):
        for j in reversed(range(len(modified_ascii[i]) - 1)):
            if modified_ascii[i][j] != empty_char and modified_ascii[i][j + 1] == empty_char:
                modified_ascii[i][j + 1], modified_ascii[i][j] = modified_ascii[i][j], empty_char
    return np.array(modified_ascii)

def rain_effect(ascii_array, empty_char=' ', rain_char='|'):
    """Simulate rain effect by adding falling rain droplets."""
    modified_ascii = [list(row) for row in ascii_array]
    for _ in range(len(modified_ascii[0]) // 4):
        drop_col = random.randint(0, len(modified_ascii[0]) - 1)
        if modified_ascii[0][drop_col] == empty_char:
            modified_ascii[0][drop_col] = rain_char
    
    for i in reversed(range(len(modified_ascii) - 1)):
        for j in range(len(modified_ascii[i])):
            if modified_ascii[i][j] == rain_char and modified_ascii[i + 1][j] == empty_char:
                modified_ascii[i + 1][j], modified_ascii[i][j] = rain_char, empty_char
    return np.array(modified_ascii)

def glitch_effect(ascii_array, empty_char=' '):
    """Simulate glitch effect by swapping random characters."""
    modified_ascii = [list(row) for row in ascii_array]
    for _ in range(len(modified_ascii) * len(modified_ascii[0]) // 10):
        x1, y1 = random.randint(0, len(modified_ascii) - 1), random.randint(0, len(modified_ascii[0]) - 1)
        x2, y2 = random.randint(0, len(modified_ascii) - 1), random.randint(0, len(modified_ascii[0]) - 1)
        modified_ascii[x1][y1], modified_ascii[x2][y2] = modified_ascii[x2][y2], modified_ascii[x1][y1]
    return np.array(modified_ascii)

def expansion_effect(ascii_array, empty_char=' '):
    """Simulate expansion effect by growing outward from the center."""
    modified_ascii = [list(row) for row in ascii_array]
    center_x, center_y = len(modified_ascii) // 2, len(modified_ascii[0]) // 2
    for i in range(len(modified_ascii)):
        for j in range(len(modified_ascii[i])):
            if modified_ascii[i][j] == empty_char and random.random() < 0.05:
                if abs(i - center_x) + abs(j - center_y) < len(modified_ascii) // 2:
                    modified_ascii[i][j] = '*'
    return np.array(modified_ascii)

def mirror_effect(ascii_array):
    """Mirror the ASCII image horizontally."""
    modified_ascii = [list(row[::-1]) for row in ascii_array]
    return np.array(modified_ascii)

def scroll_effect(ascii_array, direction='up'):
    """Scroll the ASCII image vertically up or down."""
    modified_ascii = [list(row) for row in ascii_array]
    if direction == 'up':
        modified_ascii.append(modified_ascii.pop(0))
    else:
        modified_ascii.insert(0, modified_ascii.pop())
    return np.array(modified_ascii)

def pixelation_effect(ascii_array, block_size=2, empty_char=' '):
    """Simulate pixelation effect by replacing blocks of characters with empty spaces."""
    modified_ascii = [list(row) for row in ascii_array]
    for i in range(0, len(modified_ascii), block_size):
        for j in range(0, len(modified_ascii[i]), block_size):
            if random.random() < 0.5:
                for x in range(block_size):
                    for y in range(block_size):
                        if i + x < len(modified_ascii) and j + y < len(modified_ascii[i]):
                            modified_ascii[i + x][j + y] = empty_char
    return np.array(modified_ascii)

def fire_effect(ascii_array):
    """Simulate fire effect by moving characters upwards and adding flicker."""
    modified_ascii = [list(row) for row in ascii_array]
    fire_chars = ['.', '*', '~', '^']
    for i in reversed(range(1, len(modified_ascii))):
        for j in range(len(modified_ascii[i])):
            if modified_ascii[i][j] in fire_chars:
                modified_ascii[i - 1][j] = modified_ascii[i][j]
                modified_ascii[i][j] = ' '
    for j in range(len(modified_ascii[-1])):
        if random.random() < 0.3:
            modified_ascii[-1][j] = random.choice(fire_chars)
    return np.array(modified_ascii)

def ripple_effect(ascii_array, time_step=0):
    """Simulate ripple effect expanding outward in waves."""
    modified_ascii = [list(row) for row in ascii_array]
    center_x, center_y = len(modified_ascii) // 2, len(modified_ascii[0]) // 2
    for i in range(len(modified_ascii)):
        for j in range(len(modified_ascii[i])):
            distance = math.sqrt((i - center_x)**2 + (j - center_y)**2)
            if int(distance) % 4 == time_step % 4:
                modified_ascii[i][j] = '*'
            else:
                modified_ascii[i][j] = ' '
    return np.array(modified_ascii)


def matrix_effect(modified_ascii):
    pour_symbol = random.choice("|")
    
    for i, row in reversed(list(enumerate(modified_ascii))):
        for j, char in enumerate(row):
            #print(i,j)
            #the chance of droplets is increased the closer we are to the top
            #print(i, j)
            #print(random.random(), weights[i])
            #i : 37...0
            #[0.9 ... 0]
            if weights[i]/100 > random.random():
                modified_ascii[i][j] = pour_symbol
                pour_length = random.randint(1,3)
                if i > pour_length:
                    for cell in range(pour_length):
                        modified_ascii[cell][j] = pour_symbol
            
            if weights[i]+0.3 > random.random():
                #print(i)
                if i < modified_ascii.shape[0]:
                    if modified_ascii[i-1][j]  == pour_symbol:
                        modified_ascii[i][j] = pour_symbol
            
            if i  > random.randint(0,100):
                modified_ascii[i][j] = original_ascii[i][j]
    return modified_ascii

effect_functions = [matrix_effect, pour_effect, drip_effect, wave_effect, shake_effect, swirl_effect, 
    erosion_effect, wind_effect, rain_effect, glitch_effect, expansion_effect,
    mirror_effect, scroll_effect, pixelation_effect, fire_effect, ripple_effect
]
effect_index = 0  # Start with the first effect

while True:
    #print(keyboard.read_key())
    if keyboard.is_pressed('R'):
        modified_ascii = original_ascii
    # Listen for key presses
    if keyboard.is_pressed('right'):
        effect_index = (effect_index + 1) % len(effect_functions)
        time.sleep(0.2)  # Prevent rapid switching

    if keyboard.is_pressed('left'):
        effect_index = (effect_index - 1) % len(effect_functions)
        time.sleep(0.2)
        
    
    print(effect_functions[effect_index])
    print(type(modified_ascii))
    modified_ascii = effect_functions[effect_index](modified_ascii)
    
    
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
    
    """
    #pour_symbol = random.choice("|*xoO1")
    pour_symbol = random.choice("|")
    
    for i, row in reversed(list(enumerate(modified_ascii))):
        for j, char in enumerate(row):
            #print(i,j)
            #the chance of droplets is increased the closer we are to the top
            #print(i, j)
            #print(random.random(), weights[i])
            #i : 37...0
            #[0.9 ... 0]
            if weights[i]/100 > random.random():
                modified_ascii[i][j] = pour_symbol
                pour_length = random.randint(1,3)
                if i > pour_length:
                    for cell in range(pour_length):
                        modified_ascii[cell][j] = pour_symbol
            
            if weights[i]+0.3 > random.random():
                #print(i)
                if i < modified_ascii.shape[0]:
                    if modified_ascii[i-1][j]  == pour_symbol:
                        modified_ascii[i][j] = pour_symbol
            
            if i  > random.randint(0,100):
                modified_ascii[i][j] = original_ascii[i][j]
                
    """            
    
    #modified_ascii = pour_effect(modified_ascii)
    #modified_ascii = drip_effect(modified_ascii)
    #modified_ascii = wave_effect(modified_ascii)
    #modified_ascii = shake_effect(modified_ascii)
    #modified_ascii = swirl_effect(modified_ascii)
        
    os.system('cls' if os.name == 'nt' else 'clear')
    poured_ascii_art = "\n".join("".join(row) for row in modified_ascii)
    print(poured_ascii_art)
    
    original_ascii_art = "\n".join("".join(row) for row in original_ascii)
    print(original_ascii_art)
    print(effect_functions[effect_index])
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
                        
    
    

