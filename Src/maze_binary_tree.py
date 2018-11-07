##
# @file     maze_binary_tree.py
# @author   Ferenc Nemeth
# @date     4 Nov 2018
# @brief    This script generates a maze with binary tree algorithm in Minecraft.
#
#           Copyright (c) 2018 Ferenc Nemeth - https://github.com/ferenc-nemeth/
#

import random
import numpy as np
import mcpi.minecraft as minecraft
import mcpi.block as block
import sys

# Makes the boundary walls, entrance and exit points of the maze.
def Maze_Init(mc, mc_x, mc_y, mc_z, width, height, length, material):
    # Create an area filled with material.
    maze = np.full((length,width), 0, dtype="uint8")
    mc.setBlocks(mc_x, mc_y, mc_z, mc_x+width-1, mc_y+height-1, mc_z+length-1, material)

    # Entrance and exit.
    maze[0,1] = 1
    mc.setBlocks(mc_x+1, mc_y, mc_z, mc_x+1, mc_y+height-1, mc_z, block.AIR)
    maze[length-1,width-2] = 1
    mc.setBlocks(mc_x+width-2, mc_y, mc_z+length-1, mc_x+width-2, mc_y+height-1, mc_z+length-1, block.AIR)

    return maze

# The binary tree algorithm. Randomly craves horizontally or vertically.
def Maze_CravePassage(mc, maze, mc_x, mc_y, mc_z, height):
    # Loop through every second cell.
    for z in xrange(1, maze.shape[0]-1, 2):
        for x in xrange(1, maze.shape[1]-1, 2):
            # Decide which orientation we shall crave.
            # Normally we choose randomly, except at the end sides.
            if (((maze.shape[1]-2) == x) and ((maze.shape[0]-2) == z)):
                orientation = "none"
            elif ((maze.shape[1]-2) == x):
                orientation = "vertical"
            elif ((maze.shape[0]-2) == z):
                orientation = "horizontal"
            else:
                orientation = random.choice(["horizontal", "vertical"])

            # Crave horizontally or vertically 2 cells.
            if ("horizontal" == orientation):
                maze[z, x:x+3] = 1
                mc.setBlocks(mc_x+x, mc_y, mc_z+z, mc_x+x+2, mc_y+height-1, mc_z+z, block.AIR)
            elif ("vertical" == orientation):
                maze[z:z+3, x] = 1
                mc.setBlocks(mc_x+x, mc_y, mc_z+z, mc_x+x, mc_y+height-1, mc_z+z+2, block.AIR)
            else:
                return

# Main function.
def main():
    mc = minecraft.Minecraft()
    
    # To run the script, we need the width, height, length and material of the maze.
    if (5 == len(sys.argv)):
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        length = int(sys.argv[3])
        material = block.Block.byName(sys.argv[4])

        # Make sure, that width and length are odd numbers.
        if ((not(width%2)) or (not(length%2))):
            print "Width and length must be odd numbers!"
            return

        # Get position of the player. Shift it a little, so the entrance is going to be in front of the player.
        mc_x, mc_y, mc_z = mc.player.getPos()
        mc_x -= 1
        mc_z += 2

        # Init and do the algorithm.
        maze = Maze_Init(mc, mc_x, mc_y, mc_z, width, height, length, material)
        Maze_CravePassage(mc, maze, mc_x, mc_y, mc_z, height)
        mc.postToChat("Maze generation done!")
    else:
        # If we did not get enought parameters, then send a warning.
        mc.postToChat("The following parameters are needed: width, height, length, material")
        mc.postToChat("For example: 11 2 11 stone")
    
# Starting point of the script.
if ("__main__" == __name__):
    main()
