import copy
import math
import media
import os
import os.path
import pygame
import random
from node import Tree


def game_func(node, color_dict, previous_filename):
    '''(Tree, dict, unicode) -> Nonetype
    Create a pygame window which shows all the rectangles which
    shows every files in a directory.'''

    # Create a pygame window with caption and background.
    pygame.init()
    screen_size = (1200, 700)
    pygame.display.set_caption(previous_filename)
    screen = pygame.display.set_mode(screen_size)
    filesize = node.total()  
    x, y = 0, 0
    blue = (0, 12, 0)
    running = True
    screen.fill(blue)
    tiling(node, 1200, 700, node.total(), color_dict)
    r = screen.copy()

    while running:
        
        # bliting the directory text and size text
        font_position = print_name(previous_filename, screen_size)
        screen.blit(font_position[0], font_position[1])
        font_position = print_name(str(filesize),\
                                   screen_size, font_position[2])
        screen.blit(font_position[0], font_position[1])

        event = pygame.event.poll()
        
        # stop running condition
        if event.type == pygame.QUIT:
            running = False

        # text changing as mouse moving
        elif event.type == pygame.MOUSEMOTION:
            mouse_position = event.pos
            x, y = mouse_position[0], mouse_position[1]
            filename = node.getting_range(x, y)
            filesize = filename[1]
            filename = filename[0]
            if filename != previous_filename:
		# blit the original surface back before making any change
                screen.blit(r, (0, 0))
                previous_filename = filename

        # sub-pygame window created as mouse clicked on specific file
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            x, y = mouse_position[0], mouse_position[1]
            filename = node.getting_range(x, y)
            sub_tree = node.search_tree(filename[0])
            game_func(sub_tree, color_dict, filename[0])
            pygame.display.set_caption(filename[0])  # add
            tiling(node, 1200, 700, node.total(), color_dict)
            screen.blit(r, (0, 0))

        pygame.display.update()


def _print(filename):
    '''unicode -> str
    Print the filename.'''

    print filename


def creating_tree(d, tree, color_dict={}):
    '''(unicode, Tree, dict) -> tuple (Tree, dict)
    Create a new tree with directory d and tree Tree. Return a tuple 
    consists of a Tree and a dictionary. Tree stores information of a 
    directory. Dictionary stores the colors of each type of file, colors 
    are being chosen randomly .'''

    i = 0

    for filename in os.listdir(d):
        item = os.path.join(d, filename)

        # Update the tree if the content is a folder
        if os.path.isdir(item):
            tree.insert_directory((item, os.path.getsize(item)))
            creating_tree(item, tree.child[i], color_dict)

        # Update the tree if the the content is a file
        else:
            tree.insert_files((item, os.path.getsize(item)))

            # Get the type of file and update the color_dict
            index = item.rfind(".")
            file_type = item[index:]
            if file_type not in color_dict:
                color_dict[item[index:]] = rand_color()
        i += 1

    return (tree, color_dict)


def tiling(tree, wide, high, total, color_dict, x=0, y=0):
    '''(Tree, int, int, tuple, dict, int, int) -> tuple
    Return the origin coordinate of a rectangle and tiling it.'''
 
    node_area = tree.total()
    ratio = float(node_area) / total
    # get the ratio of current node in the whole display
    orientation = order(wide, high, ratio)
    width, height = orientation[0], orientation[1]
    x_range, y_range = range(x, x + width), range(y, y + height)
    tree._range = (x_range, y_range)    
    # setting the range of a tree which is all x-coordinate and
    # y-coordinate that the tree occupies

    if type(tree) == Tree:
        pygame.draw.rect(pygame.display.get_surface(), \
                         (255, 255, 255), (x, y, width, height))
        coor = (x, y)

        for child in tree.child:
	    # for every child inside the tree do recursion of the function
            coor = tiling(child, width, height, node_area,\
                          color_dict, gradient, coor[0], coor[1])
        pygame.draw.rect(pygame.display.get_surface(),\
                         (255, 255, 255), (x, y, width, height), 1)
    else:
        color = file_color(tree, color_dict)
        if orientation[2] == "h":
            change_in = width
        else:
            change_in = height
        r, g, b = color[0], color[1], color[2]
        for i in range(0, change_in):
	    if gradient:
		ratio = 1
	    else:
		ratio = float(i)/change_in
		# to make the rectangle fill in with gradient color

            new_r = int(ratio * r)
            new_g = int(ratio * g)
            new_b = int(ratio * b)
            new_color = (new_r, new_g, new_b)
            if orientation[2] == "h":
                pygame.draw.rect(pygame.display.get_surface(),\
                                 new_color, (x + i, y, 1, height))
            else:
                pygame.draw.rect(pygame.display.get_surface(),\
                                 new_color, (x, y + i, width, 2))

    if orientation[2] == "h":
        x += width
    else:
        y += height

    return (x, y)



def order(wide, high, ratio):
    '''(int, int, float) -> (int, int, str)
    Return the width and height and the orientation of a rectangle.'''

    if wide > high:
        return int(round(wide * ratio)), high, "h"
    else:
        return wide, int(round(ratio * high)), "v"


def rand_color():
    '''None -> tuple
    Return a tuple which repesents a color that being chosen randomly.'''

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    while (r, g, b) == (255, 255, 255):
        return rand_color()
    return (r, g, b)


def file_color(tree, color_dict):
    '''(Tree, dict) -> tuple
    If color_dict is empty, choose and return a color randomly. If the 
    color of this type of file is in color_dict, find and return it.'''

    if color_dict == {}:
        color = rand_color()
    else:
        index = tree.key[0].rfind(".")
        file_type = tree.key[0][index:]
        color = color_dict[file_type]

    return color


def print_name(previous_filename, screen_size, previous_height=0):
    '''(unicode, tuple, int) -> tuple(object, tuple, int)
    Set the text color and font, create text_surface.
    Return the text_surface, text's start position and height as a tuple.'''

    white = (255, 255, 255)
    font = pygame.font.Font(None, 30)
    text_surface = font.render(previous_filename, 1, white)

    text_h = font.get_height()
    text_w = font.get_linesize()
    text_pos = (0, (screen_size[1] - 1 - text_h - previous_height))

    return (text_surface, text_pos, text_h)


if __name__ == '__main__':

    tree = Tree()

    # ask the user to choose a directory
    d = media.choose_folder()
    tree.insert_directory((d, os.path.getsize(d)))

    # ask the user to choose whether file is colored according to filetype
    color = raw_input("Do you want files colored according to \
their filetype?(yes or no)")
    while color != "yes" and color != "no":
        color = raw_input("Do you want files colored according \
to their filetype?(yes or no)")
    
    # ask the user whether to use gradient choice
    gradient = raw_input("Do you want files colored plain \
    or gradient? (p or g)\n" )
    while gradient != "p" and color != "g":
	gradient = raw_input("Do you want files colored plain? (p or g)\n" )
  
    # display the files according to user's choice
    i = creating_tree(d, tree)
    if gradient == "p":
	gradient = True

    else:
	gradient = False

    if color == "yes":
	game_func(i[0],i[1], d, gradient)
    else:
	game_func(i[0],{}, d, gradient)
