##
# @file     maze_recursive_division.py
# @author   Ferenc Nemeth
# @date     4 Nov 2018
# @brief    This script generates a maze with recursive division algorithm in Minecraft.
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
    # Create an empty area.
    maze = np.full((length, width), 1, dtype="uint8")

    # Boundary walls.
    maze[0, :] = 0
    mc.setBlocks(mc_x, mc_y, mc_z, mc_x+width-1, mc_y+height-1, mc_z, material)
    maze[length-1, :] = 0
    mc.setBlocks(mc_x, mc_y, mc_z+length-1, mc_x+width-1, mc_y+height-1, mc_z+length-1, material)
    maze[:, 0] = 0
    mc.setBlocks(mc_x, mc_y, mc_z, mc_x, mc_y+height-1, mc_z+length-1, material)
    maze[:, width-1] = 0
    mc.setBlocks(mc_x+width-1, mc_y, mc_z, mc_x+width-1, mc_y+height-1, mc_z+length-1, material)

    # Entrance and exit.
    maze[0,1] = 1
    mc.setBlocks(mc_x+1, mc_y, mc_z, mc_x+1, mc_y+height-1, mc_z, block.AIR)
    maze[length-1, width-2] = 1
    mc.setBlocks(mc_x+width-2, mc_y, mc_z+length-1, mc_x+width-2, mc_y+height-1, mc_z+length-1, block.AIR)

    return maze

# The recursive division algorithm. It places the walls + holes randomly.
def Maze_Divide(mc, maze, mc_x, mc_y, mc_z, x, z, width, height, length, material):
    # Decide what orientation the wall should be placed.
    if (width < length):
        orientation = "horizontal"
    elif (width > length):
        orientation = "vertical"
    else:
        orientation = random.choice(["horizontal", "vertical"])

    # Horizontal.
    if ("horizontal" == orientation):
        # If there is not enought space, stop.
        if (5 > length):
            return

        # Randomly get the wall's and the hole's position.
        wall = z + (random.randint(2, length-3)//2*2)
        hole = x + (random.randint(1, width-2)//2*2+1)

        # Place the wall.
        for i in range(x, x+width-1):
            maze[wall, i] = 0
            mc.setBlocks(mc_x+i, mc_y, mc_z+wall, mc_x+i, mc_y+height-1, mc_z+wall, material)

        # Place the hole
        maze[wall, hole] = 1
        mc.setBlocks(mc_x+hole, mc_y, mc_z+wall, mc_x+hole, mc_y+height-1, mc_z+wall, block.AIR)

        # Calculate the new values for the next run.
        width_new = width
        length_new = wall-z+1
        # Complementary pairs. 'The other side of the wall.'
        x_pair = x
        z_pair = wall
        width_new_pair = width
        length_new_pair = z+length-wall

    # Vertical.
    elif ("vertical" == orientation):
        # If there is not enought space, stop.
        if (5 > width):
            return

        # Randomly get the wall's and the hole's position.
        wall = x + (random.randint(2, width-3)//2*2)
        hole = z + (random.randint(1, length-2)//2*2+1)

        # Place the wall.
        for i in range(z, z+length-1):
            maze[i, wall] = 0
            mc.setBlocks(mc_x+wall, mc_y, mc_z+i, mc_x+wall, mc_y+height-1, mc_z+i, material)

        # Place the hole.
        maze[hole, wall] = 1
        mc.setBlocks(mc_x+wall, mc_y, mc_z+hole, mc_x+wall, mc_y+height-1, mc_z+hole, block.AIR)

        # Calculate the new values for the next run.
        width_new = wall-x+1
        length_new = length
        # Complementary pairs. 'The other side of the wall.'
        x_pair = wall
        z_pair = z
        width_new_pair = x+width-wall
        length_new_pair = length
    else:
        # Error. Not horizontal and not vertical? WTF?
        return

    # Call it again.
    Maze_Divide(mc, maze, mc_x, mc_y, mc_z, x, z, width_new, height, length_new, material)
    # When there are no more places left, then go to the 'other side'.
    Maze_Divide(mc, maze, mc_x, mc_y, mc_z, x_pair, z_pair, width_new_pair, height, length_new_pair, material)

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
        Maze_Divide(mc, maze, mc_x, mc_y, mc_z, 0, 0, width, height, length, material)
        mc.postToChat("Maze generation done!")
    else:
        # If we did not get enought parameters, then send a warning.
        mc.postToChat("The following parameters are needed: width, height, length, material")
        mc.postToChat("For example: 11 2 11 stone")

# Starting point of the script.
if ("__main__" == __name__):
    main()
