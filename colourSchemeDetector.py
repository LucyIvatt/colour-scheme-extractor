from sklearn.cluster import KMeans
import pygame
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
import sys

DARK_GREY = (33, 37, 43)
LIGHT_GREY = (41, 45, 53)

def rgb_to_hex(colour):
    hex_values = [hex(int(value)) for value in colour]
    final_string = "#"
    for value in hex_values:
        sub_string = str(value).lstrip("0x")
        if len(sub_string) != 2:
            sub_string = "0" + sub_string
        final_string += sub_string
    return final_string

def read_image(file_path):
    try:
        image = cv2.imread(file_path) # Reads the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Converts from BGR to RGB
    except cv2.error:
        print(file_path, "is an Invalid file path, please try again.")
        sys.exit()
    return image

def get_colours(image):
    global colour_number
    # Resizes the image where no size is > 500 while maintaining the aspect ratio
    h, w, _ = image.shape
    if h > w:
        ratio = w / h
        edited_image = cv2.resize(image, (int(500 * ratio), 500), interpolation = cv2.INTER_AREA)
    else:
        ratio = h / w
        edited_image = cv2.resize(image, (500, int(500 * ratio)), interpolation = cv2.INTER_AREA)
    edited_image = edited_image.reshape(edited_image.shape[0] * edited_image.shape[1], 3)

    # Clusters the pixels
    clf = KMeans(n_clusters = colour_number)
    labels = clf.fit_predict(edited_image)

    counts = Counter(labels)
    center_colours = clf.cluster_centers_

    # Get ordered colours by iterating through keys
    ordered_colours = [center_colours[i] for i in counts.keys()]
    rgb_colours = [tuple(ordered_colours[i].tolist()) for i in counts.keys()]

    return rgb_colours

def draw_swatches(rgb_colours):
    global colour_number
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Helvetica', 20)
    screen = pygame.display.set_mode((150 * colour_number, 130))
    x_rectangle_coord = 0
    alternate = 1
    for i in range(colour_number):
        alternate *= -1
        if alternate == 1:
            title = DARK_GREY
        else:
            title = LIGHT_GREY
        pygame.draw.rect(screen, x[i], (x_rectangle_coord,0, 150, 100))
        pygame.draw.rect(screen, title, (x_rectangle_coord,100, 150, 30))
        hexcode = font.render(rgb_to_hex(rgb_colours[i]), False, (240, 240, 240))
        screen.blit(hexcode, (x_rectangle_coord + (150 - hexcode.get_width()) // 2, 100 + (30 - hexcode.get_height()) // 2))
        x_rectangle_coord += 150
    pygame.display.update()
    print("Press enter to close the swatch")
    swatch_open = True
    while swatch_open:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.QUIT
                    swatch_open = False
    
if __name__ == '__main__':
    program_open = True
    while program_open:
        try:
            colour_number = int(input("How many colours would you like? "))
        except:
            print("Invalid input, please enter a number")
            continue
        image_path = input("What is the file path of the image you wish to use? ")
        x = get_colours(read_image(image_path))
        draw_swatches(x)
        user_input_continue = input("Swatch Complete! Press 1 to analyse another image or 0 to exit: ")
        if user_input_continue == "0":
            program_open = False
