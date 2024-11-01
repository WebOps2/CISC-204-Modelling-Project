# CISC/CMPE 204 Modelling Project Group 12 2048 Game

Welcome to our project modeling the 2048 game!

The idea of the game of 2048 is that you move and merge tiles with equivalent values to generate tiles with larger values. The grid on which you can move the tile is a 4 * 4 grid. Every time you can move in one of the four directions: up, down, left, right. Once a tile with value 2048 is being created, you win; if there is a deadlock, which means there are no possible ways to further make a move or merge, you lose the game. We would like to model the logic behind this game. Particularly we would like to model the mechanics of movements. We will be diving into the status of each tile before and after movements, whether they can move, and toward which direction they are moving. 

## Structure

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `run.py`: General wrapper script that you can choose to use or not. Only requirement is that you implement the one function inside of there for the auto-checks.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
