# minecraft-maze-generator
Maze generator scripts for Minecraft.

### Table of content
- [Introduction](#introduction)
- [How it works](#how-it-works)
- [How to use it](#how-to-use-it)
- [References](#references)

### Introduction
A maze generator for Minecraft with three different algorithms.

### How it works

***[See my demostration video on youtube.](https://www.youtube.com/watch?v=cERIEOcE1S4)***

There are three maze generator Python scripts:
- Recursive division [[1]](#references)
- Recursive backtracking [[2]](#references)
- Binary Tree [[3]](#references)

The dimensions and the material of the maze can be changed.<br> The maze is always generated to the south of the player.

<img src="https://raw.githubusercontent.com/ferenc-nemeth/minecraft-maze-generator/master/Design/maze_example.png" > <br>
*Figure 1. Generated mazes.*

### How to use it
Install Minecraft, Python 2.7, numpy and Raspberry Jam Mod to run the scripts [[4]](#references).
Then you can run the generators with the following command:
```
/py maze_<algorithm> <width> <height> <length> <block>
```

For example:
```
/py maze_recursive_division 21 2 21 pink_wool
/py maze_recursive_backtracking 15 1 55 obsidian
/py maze_binary_tree 35 5 35 diamond_ore
```

### References
[1] [Wikipedia - Recursive divison method](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_division_method)<br>
[2] [Wikipedia - Recursive backtracking method](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)<br>
[3] [Wikipedia - Binary tree method](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Simple_algorithms)<br>
[4] [Iinstructable- Python coding for Minecraft](https://www.instructables.com/id/Python-coding-for-Minecraft/)<br>
