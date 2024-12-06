
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
import random
import copy

# Encoding that will store all of your constraints
E = Encoding()

# we want to build a list which has four lists nested in them to represent the grid (each lists are initialized empty)
GRID = []
# l = 0   

LOCATION = []
for row in range(1, 5):
    for col in range(1, 5):
        LOCATION.append((row, col))
        
ORIENTATION = ['U', 'D', 'L', 'R']

# create a 4x4 grid with all elements initialized to (0, 0)
for i in range(1, 5):
    GRID_COLS= []
    for j in range(1, 5):
        GRID_COLS.append((0, 0))
    GRID.append(GRID_COLS)

# initialize the board to have 1 tile in it
# tempLoc = random.choice(LOCATION)
# GRID[tempLoc[0]-1][tempLoc[1]-1] = tempLoc
def generate_tile(x, y):
    GRID[x - 1][y - 1] = (x,y)
# GRID[0][0] = (1, 1)
# GRID[1][0] = (2, 1)
# GRID[2][0] = (3, 1)
# GRID[3][0] = (4, 1)
# GRID[1][0] = (2, 1) 

    
print(GRID)

# we want to build a 4x4 grid which has 16 locations, the structure of the grid should be a 2D array, with each element being a list of four locations
# each location is represented by a tuple (x, y) where x is the row number and y is the column number
# for i in range(1, 5):
#     GRID_COLS= []
#     for j in range(1, 5):
#         GRID_COLS.append((i, j))
#     GRID.append(GRID_COLS)

# print(GRID)
# we actually don't need GRID to be filled at this point, we will update it later while doing constraints

# representing timestep
AtTime = 0
move = False


TIMESTEP = []
for t in range(0, 16):
    TIMESTEP.append(f"t_{t}")
    
print(TIMESTEP)


@proposition(E)
class Location(object):
    def __init__(self, loc, timeStep):
        assert loc in LOCATION
        assert timeStep in TIMESTEP
        self.loc = loc
        self.timeStep = timeStep
    def _prop_name(self):
        return f"{self.loc} occupied @ {self.timeStep}"


@proposition(E)
class MoveUp(object):
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveUp @ {self.timeStep}"
    
@proposition(E)
class MoveDown(object):
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveDown @ {self.timeStep}"

@proposition(E)
class MoveLeft(object):
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveLeft @ {self.timeStep}"

@proposition(E)
class MoveRight(object):
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveRight @ {self.timeStep}"

@proposition(E)
class AbleToMove(object):
    def __init__(self, loc, orientation, timeStep):
        assert timeStep in TIMESTEP
        assert loc in LOCATION
        assert orientation in ORIENTATION
        self.timeStep = timeStep
        self.loc = loc
        self.orientation = orientation
    def _prop_name(self):
        return f"{self.loc} canMove along {self.orientation} @ {self.timeStep}"


@proposition(E)
class Random(object):
    def __init__(self, loc, timeStep):
        assert loc in LOCATION
        assert timeStep in TIMESTEP
        self.loc = loc
        self.timeStep = timeStep
    def _prop_name(self):
        return f"{self.loc} randomly filled @ {self.timeStep}"
    
def test_first_row_full():
    for col in range(1, 5):
        generate_tile(1, col)
    E.add_constraint(AbleToMove())

# @constraint(E)

# we want to start the grid with a random location (x, y) being filled 
# 

# TODO make a function that actually does the movement (at a particular timeStep), after that we add a constriant moveDirection(timeStep) that returns true if the player has moved at that timeStep

# TODO make able_to_move of a tuple (x, y) at timestep t a constraint from recursion

# TODO timestep cannot go back is a constraint

# TODO when we cannot move at least one of the directions, we cannot move in that direction & we make timeStep unchanged

# TODO loc(x,y,t) cannot be both true and false

# TODO create a constraint moveup(t) that takes in a timestep and returns true if the player has moved at that timestep

# TODO we have to make sure that (1, 1) cannot be at place other than (1, 1) at any timestep


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html

# @constraint.at_least_one(E)
# @proposition(E)
# class FancyPropositions:

#     def __init__(self, data):
#         self.data = data

#     def _prop_name(self):
#         return f"A.{self.data}"


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # E = Encoding()
    
    global AtTime
    global move
    
    for row in range(0,4):
        for col in range(0, 4):
            if GRID[row][col] == (row +1, col + 1):
                E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]))
            elif GRID[row][col] == (0, 0):
                E.add_constraint(~Location((row + 1, col+ 1), TIMESTEP[AtTime]))
    for row in range(0,4):
        for col in range(0, 4):
            if GRID[row][col] == (0,0):
                E.add_constraint( ~AbleToMove((row + 1, col + 1), 'U', TIMESTEP[AtTime]) &  ~AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]) &  ~AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]) &  ~AbleToMove((row + 1, col + 1), 'L', TIMESTEP[AtTime]))
                
    for row in range(0,4):
        for col in range(0, 4):
            if row == 0:
                E.add_constraint(~AbleToMove((row + 1, col + 1), 'U', TIMESTEP[AtTime]))
            if row == 3:
                E.add_constraint(~AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]))
            if col == 0:
                E.add_constraint(~AbleToMove((row + 1, col + 1), 'L', TIMESTEP[AtTime]))
            if col == 3:
                E.add_constraint(~AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]))
            
    for row in range(0,4):
        for col in range(0,4):
            if row != 0 and GRID[row][col] == (row +1, col + 1) and GRID[row - 1][col] == (0,0):
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) & ~Location((row, col + 1), TIMESTEP[AtTime]) >> AbleToMove((row + 1, col + 1), 'U', TIMESTEP[AtTime]))
            
    for row in range(0,4):
        for col in range(0,4):
            if row != 3 and GRID[row][col] == (row +1, col + 1)  and GRID[row + 1][col] == (0,0):
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) & ~Location((row + 2, col + 1), TIMESTEP[AtTime]) >> AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]))
            
    # def moveU(): 
    #     E.add_constraint(MoveUp('t_1'))
    for row in range(0,4):
        for col in range(0,4):
            if col != 0 and GRID[row][col] == (row +1, col + 1) and GRID[row][col - 1] == (0,0):
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) & ~Location((row + 1, col), TIMESTEP[AtTime]) >> AbleToMove((row + 1, col + 1), 'L', TIMESTEP[AtTime]))
    for row in range(0,4):
        for col in range(0,4):
            if col != 3 and GRID[row][col] == (row +1, col + 1) and GRID[row][col + 1] == (0,0):
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) & ~Location((row + 1, col + 2), TIMESTEP[AtTime]) >> AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]))
                
    
    r_int = random.randint(0,3)
    # print(r_int)
    Orientation = ORIENTATION[r_int]
    
    # Orientation = 'U'
    # print(Orientation)
    # if Orientation == 'U':
    #     E.add_constraint(MoveUp(TIMESTEP[AtTime]))
    
    # Write constraint of We can attempt to move the graph regardless if one loc can a=move or not. 
    for row in range(0,4):
        for col in range(0,4):
            if Orientation == 'U' and row != 0 and GRID[row][col] == (row +1, col + 1) and GRID[row - 1][col] == (0,0):
                E.add_constraint(AbleToMove((row + 1, col + 1), 'U', TIMESTEP[AtTime]) & MoveUp(TIMESTEP[AtTime]))
                break
            elif Orientation == 'D' and row != 3 and GRID[row][col] == (row +1, col + 1)  and GRID[row + 1][col] == (0,0):
                E.add_constraint(AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]) & MoveDown(TIMESTEP[AtTime]))
                break
            elif Orientation == 'L' and col != 0 and  GRID[row][col] == (row +1, col + 1) and GRID[row][col - 1] == (0,0):
                E.add_constraint(AbleToMove((row + 1, col + 1), 'L', TIMESTEP[AtTime]) & MoveLeft(TIMESTEP[AtTime]))
                break
            elif Orientation == 'R' and col != 3 and GRID[row][col] == (row +1, col + 1) and GRID[row][col + 1] == (0,0):
                E.add_constraint(AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]) & MoveRight(TIMESTEP[AtTime]))
                break
    
    def UpMove(x,y):
        if x == 0 or GRID[x-1][y] != (0, 0):
            return 
        if GRID[x][y] != (0,0):
            # move the tile up and update its coordinates (only updates the x coordinate)
            GRID[x-1][y] = (x, GRID[x][y][1]) 
            GRID[x][y] = (0, 0)
            UpMove(x - 1, y)   
              
    def DownMove(x,y):
        if x == 3 or GRID[x+1][y] != (0, 0):
            return
        
        if GRID[x][y] != (0, 0):
            # move the tile down and update its coordinates (only updates the x coordinate)
            GRID[x+1][y] = (x+2, GRID[x][y][1]) 
            GRID[x][y] = (0, 0)

            DownMove(x + 1, y) 
    def LeftMove(x,y):
        if y == 0 or GRID[x][y-1] != (0, 0):
            return
        
        if GRID[x][y] != (0, 0):
            # move the tile left and update its coordinates (only updates the y coordinate)
            GRID[x][y-1] = (GRID[x][y][0], y) 
            GRID[x][y] = (0, 0)

            LeftMove(x, y - 1) 
    def RightMove(x,y):
        if y == 3 or GRID[x][y+1] != (0, 0):
            return
        
        if GRID[x][y] != (0, 0):
            # move the tile right and update its coordinates (only updates the y coordinate)
            GRID[x][y+1] = (GRID[x][y][0], y+2) 
            GRID[x][y] = (0, 0)

            RightMove(x, y + 1)
    
    def DistanceUp(x, y):
        if x == 0 or GRID[x-1][y] != (0, 0):
            return 0

        else: 
            return 1 + DistanceUp(x - 1, y)
    def DistanceDown(x, y):
        if x == 3 or GRID[x+1][y] != (0, 0):
            return 0

        else: 
            return 1 + DistanceDown(x + 1, y)
    def DistanceLeft(x, y):
        if y == 0 or GRID[x][y-1] != (0, 0):
            return 0

        else: 
            return 1 + DistanceLeft(x, y - 1)
    def DistanceRight(x, y):
        if y == 3 or GRID[x][y+1] != (0, 0):
            return 0
        else: 
            return 1 + DistanceRight(x, y + 1)
    
        
    GridTemp = copy.deepcopy(GRID)  
    if Orientation == 'D':
        row = 3       
        while  row > -1:
            for col in range(0, 4):
                if row != 3 and GRID[row][col] != (0,0) and GRID[row + 1][col] == (0,0):
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]) & MoveDown(TIMESTEP[AtTime]) >> Location((row + 1 + DistanceDown(row, col) , col + 1), TIMESTEP[AtTime + 1]))
                    DownMove(row, col) 
            row -= 1
    elif Orientation == 'R':
        for row in range(0,4):
            col = 3  
            while col > - 1:
                if col != 3 and GRID[row][col] != (0,0) and GRID[row][col + 1] == (0,0):
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]) & MoveRight(TIMESTEP[AtTime]) >> Location((row + 1 , col + 1 + DistanceRight(row, col)), TIMESTEP[AtTime + 1]))
                    RightMove(row, col) 
                col -= 1
             
    for row in range(0,4):
        for col in range(0,4):
                if row != 0 and GRID[row][col] != (0,0) and GRID[row - 1][col] == (0,0) and Orientation == 'U':
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'U', TIMESTEP[AtTime]) & MoveUp(TIMESTEP[AtTime]) >> Location((row + 1 - DistanceUp(row, col) , col + 1), TIMESTEP[AtTime + 1]))
                    # print(TIMESTEP[AtTime])
                    UpMove(row, col)
                    
                    # E.add_constraint()
                elif row != 3 and GRID[row][col] != (0,0) and GRID[row + 1][col] == (0,0) and Orientation == 'D':
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]) & MoveDown(TIMESTEP[AtTime]) >> Location((row + 1 + DistanceDown(row, col) , col + 1), TIMESTEP[AtTime + 1]))
                    DownMove(row, col)
                   
                    
                elif col != 0 and GRID[row][col] != (0,0) and GRID[row][col - 1] == (0,0) and Orientation == 'L':
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'L', TIMESTEP[AtTime]) & MoveLeft(TIMESTEP[AtTime]) >> Location((row + 1 , col + 1 - DistanceLeft(row, col)), TIMESTEP[AtTime + 1]))
                    LeftMove(row, col)
                    
                elif col != 3 and GRID[row][col] != (0,0) and GRID[row][col + 1] == (0,0) and Orientation == 'R':
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]) & MoveRight(TIMESTEP[AtTime]) >> Location((row + 1 , col + 1 + DistanceRight(row, col)), TIMESTEP[AtTime + 1]))
                    RightMove(row, col)
          
    # print(f"temp grid {GridTemp}")
    # print(f"Our Grid {GRID}")    
    def RandomFill():
        # we want to randomly fill a location that is empty
        emptyLoc = []
        for row in range(0,4):
            for col in range(0,4):
                if GRID[row][col] == (0,0):
                    emptyLoc.append((row + 1, col + 1))
        randomLoc = random.choice(emptyLoc)
        GRID[randomLoc[0]-1][randomLoc[1]-1] = randomLoc
        return randomLoc       
    if GridTemp == GRID: 
        move = False
        if Orientation == 'U':
            print('MoveUp is False')
            E.add_constraint(~MoveUp(TIMESTEP[AtTime]))
        if Orientation == 'D':
            print('MoveDown is False')
            E.add_constraint(~MoveDown(TIMESTEP[AtTime]))
        if Orientation == 'L':
            print('MoveLeft is False')
            E.add_constraint(~MoveLeft(TIMESTEP[AtTime]))
        if Orientation == 'R':
            print('MoveRight is False')
            E.add_constraint(~MoveRight(TIMESTEP[AtTime]))
    else:
        random_loc = RandomFill()
        E.add_constraint(~Location(random_loc, TIMESTEP[AtTime]) >> Random(random_loc, TIMESTEP[AtTime + 1]))
    
    
    #  If a loc on the grid has a tile on it then a random tile cannot be placed at that location
    for row in range(0,4):
        for col in range(0,4):
            if GRID[row][col] != (0,0) and AtTime < 15:
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) >> ~Random((row + 1, col + 1), TIMESTEP[AtTime + 1]))
  
        

    return E


if __name__ == "__main__":
    # l = 0
    generate_tile(1, 1)
    # print(GRID)
    # if move == 2
    
    # T = example_theory()
    
    def run_2048_simulation():
        global AtTime
        while AtTime < 15:
            # print(GRID)  
            # print(f"Our Grid {GRID}")           
            if move == True: 
                # print('Good') 
                AtTime += 1  
                
            T = example_theory()
            # Don't compile until you're finished adding all your constraints!
            T = T.compile()
            
            # print(T)
            # After compilation (and only after), you can check some of the properties
            # of your model:
            S = T.solve()
            # print(S)
            
            if S:
                t = set()
                s = False
                for k in S:
                    if S[k] and (f"@ t_{AtTime}" in str(k)) :
                        print(k)
                        s = True
                        t.add(str(k))
                # l += 1
                if s and AtTime < 15:       
                    print(f"\n\n Our Grid updated: {GRID} ")                  
            else:
                print('Aw man')
        print("\nSatisfiable: %s" % T.satisfiable())
        print("# Solutions: %d" % count_solutions(T))
    run_2048_simulation()
        
        
    
        # print("   Solution: %s" % T.solve())

    #E.introspect()
    
    # print("\nVariable likelihoods:")
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     # Ensure that you only send these functions NNF formulas
    #     # Literals are compiled to NNF here
    #     print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
