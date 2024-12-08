# CISC/CMPE 204 Modelling Project Group 12 2048 Game 

Welcome to our project modeling the 2048 game! We focus on the mechanics of the movements of the tiles only without considering merges of tiles. 

The idea of the classical game of 2048 is that you move and merge tiles with equivalent values to generate tiles with larger values. We do not consider the merging functions, so we do not consider the numbers appearing on each tiles either. We are interested in only the movement mechanics of the tiles. The grid on which you can move the tile is a 4 * 4 grid. 
We want to start from a grid with only one randomly generated tile on it, and let the SAT solver determine in which of the four directions it can move and chooses a movable direction to implement the movement. We use a parameter of time to indicate our steps of movements. Since the grid starts with 1 tile at time 0, we expect the grid to be filled after 15 valid movements. 

## Requirements
- `nnf`
- `bauhaus`
- `Docker`

## Structure

* `documents`: Contains folders for both of our draft and final submissions. README.md files are included in both.
* `run.py`: For our python code, this is the only file you will have to look at. We have all our propositions and several testing functions in it. This is the file containing our example theory, which has all our constraints. 
* `test.py`: Just a default file from Professor Muise to confirm that our submission has everything required. This essentially just means it will check for the right files and sufficient theory size.

## Running With Docker

We are using a dockerfile. We have built an image called 
`cisc204`
We tie the folder `/PROJECT` in the container with the folder in our local directory.
