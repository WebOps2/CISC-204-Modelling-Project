
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
tempLoc = random.choice(LOCATION)
GRID[tempLoc[0]-1][tempLoc[1]-1] = tempLoc
# GRID[3][0] = (4, 1)
    
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

TIMESTEP = []
for t in range(0, 16):
    TIMESTEP.append(f"t_{t}")
    
print(TIMESTEP)


@proposition(E)
class Location:
    def __init__(self, loc, timeStep):
        assert loc in LOCATION
        assert timeStep in TIMESTEP
        self.loc = loc
        self.timeStep = timeStep
    def _prop_name(self):
        return f"{self.loc} occupied @ {self.timeStep}"


@proposition(E)
class MoveUp:
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveUp @ {self.timeStep}"
    
@proposition(E)
class MoveDown:
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveDown @ {self.timeStep}"

@proposition(E)
class MoveLeft:
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveLeft @ {self.timeStep}"

@proposition(E)
class MoveRight:
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveRight @ {self.timeStep}"

@proposition(E)
class AbleToMove:
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
class Random:
    def __init__(self, loc, timeStep):
        assert loc in LOCATION
        assert timeStep in TIMESTEP
        self.loc = loc
        self.timeStep = timeStep
    def _prop_name(self):
        return f"{self.loc} randomly filled @ t_{self.timeStep}"

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

@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    
    # TODO if we are at the edge of the grid, we cannot move in that direction
    
    # if the row number (x) is not 1 and the location above (x, y) is true, then the location (x-1, y) is true
    for timeStep in TIMESTEP:
        for loc in LOCATION:
            if loc[0] != 1:
                E.add_constraint(Location(loc, timeStep) & ~Location((loc[0] - 1, loc[1]), timeStep) >> AbleToMove(loc, 'U', timeStep))
            elif loc[0] == 1:
                E.add_constraint(~AbleToMove(loc, 'U', timeStep))

    # if the row number (x) is not 4 and the location below (x, y) is true, then the location (x+1, y) is true
    for timeStep in TIMESTEP:
        for loc in LOCATION:
            if loc[0] != 4:
                E.add_constraint(Location(loc, timeStep) & ~Location((loc[0] + 1, loc[1]), timeStep) >> AbleToMove(loc, 'D', timeStep))
            elif loc[0] == 4:
                E.add_constraint(~AbleToMove(loc, 'D', timeStep))
    
    # if the col number (y) is not 1 and the location on the left of (x, y) is true, then the location (x, y-1) is true
    for timeStep in TIMESTEP:
        for loc in LOCATION:
            if loc[1] != 1:
                E.add_constraint(Location(loc, timeStep) & ~Location((loc[0], loc[1] - 1), timeStep) >> AbleToMove(loc, 'L', timeStep))
            elif loc[1] == 1:
                E.add_constraint(~AbleToMove(loc, 'L', timeStep))
    
    # if the col number (y) is not 4 and the location on the right of (x, y) is true, then the location (x, y+1) is true
    for timeStep in TIMESTEP:
        for loc in LOCATION:
            if loc[1] != 4:
                E.add_constraint(Location(loc, timeStep) & ~Location((loc[0], loc[1] + 1), timeStep) >> AbleToMove(loc, 'R', timeStep))
            elif loc[1] == 4:
                E.add_constraint(~AbleToMove(loc, 'R', timeStep))
        
            
    # able_to_move: being able to move is an important thing to know of course, but it may not need to be represented as a proposition. Rather I think it may be better represented as a constraint. A tile is able to move if there is an empty space anywhere along the direction of movement.
    # essentially we want to determine if the location (x, y) can move in the direction of movement
    # if the location (x, y) is true and the orientation is up, then the location (x-1, y) is true
    for timeStep in TIMESTEP:
        for loc in LOCATION:
            if loc[0] != 1:
                E.add_constraint(Location(loc, timeStep) & MoveUp(timeStep) >> Location((loc[0] - 1, loc[1]), timeStep))
    
    # we check if at each timeStep location at (x, y) is empty or not            
    for timeStep in TIMESTEP:
        for loc in LOCATION:
            for gridPoint in GRID:
                if loc in gridPoint:
                    E.add_constraint(Location(loc, timeStep))
                E.add_constraint(~Location(loc, timeStep))
    
    
    # TODO only one of the directions can be true at a time
    # we want to make sure that movements are done in exactly 1 out of 4 directions
    for timeStep in TIMESTEP:
            for loc in LOCATION:
                constraint.add_exactly_one(E, MoveUp(timeStep) | MoveDown(timeStep) | MoveLeft(timeStep) | MoveRight(timeStep))
                
    
    
    # TODO randomly fill one location that is empty (i.e. not in the array GRID) and then update GRID
    def RandomFill():
        # we want to randomly fill a location that is empty
        emptyLoc = []
        for loc in LOCATION:
            if loc not in GRID:
                emptyLoc.append(loc)
        randomLoc = random.choice(emptyLoc)
        # print(randomLoc)
        GRID[randomLoc[0]-1][randomLoc[1]-1] = randomLoc
        
        return randomLoc
        
    # print(RandomFill())
    # we want to randomly fill a location that is empty at a particular timeStep 
    # for timeStep in TIMESTEP:
    #     E.add_constraint(Random(RandomFill(), timeStep))
    
    # we want to make sure that random are mutually exclusive
    for timeStep in TIMESTEP:
        randomList = []
        for loc in LOCATION:
            if loc in GRID:
                randomList.append(Random(loc, timeStep))
        constraint.add_exactly_one(E, randomList)
    
    # TODO when a location is filled, we cannot randomly generate something in that location
    # we want to make sure that ~empty -> ~ random
    for timeStep in TIMESTEP:
        for loc in LOCATION:
            E.add_constraint(~Location(loc, timeStep) >> ~Random(loc, timeStep))
    
    # recursive function to move the tile up, also updates the GRID
    def UpMove(x,y):
        if x == 0 or GRID[x-1][y] != (0, 0):
            return
        
        if GRID[x][y] != (0, 0):
            # move the tile up and update its coordinates (only updates the x coordinate)
            GRID[x-1][y] = (x, GRID[x][y][1]) 
            GRID[x][y] = (0, 0)

            UpMove(x - 1, y)
    
    # recursive function to move the tile down, also updates the GRID
    def DownMove(x,y):
        if x == 3 or GRID[x+1][y] != (0, 0):
            return
        
        if GRID[x][y] != (0, 0):
            # move the tile down and update its coordinates (only updates the x coordinate)
            GRID[x+1][y] = (x, GRID[x][y][1]) 
            GRID[x][y] = (0, 0)

            DownMove(x + 1, y)

    def Move(orientation):
        # make a deep copy of the grid for later comparison
        GridTemp = copy.deepcopy(GRID)
        global AtTime
        
        if orientation == "U":
            for x in range(0, 4):
                for y in range(0, 4):
                    UpMove(x, y)        
            if GRID != GridTemp:
                E.add_constraint(Random(RandomFill(), TIMESTEP[AtTime]))
                E.add_constraint(MoveUp(TIMESTEP[AtTime]))
                # this version of calling the timeStep work
                AtTime += 1
            else:
                E.add_constraint(~MoveUp(TIMESTEP[AtTime]))
        elif orientation == "D":
            for x in range(0, 4):
                for y in range(0, 4):
                    DownMove(x, y)
            if GRID != GridTemp:
                E.add_constraint(Random(RandomFill(), TIMESTEP[AtTime]))
                E.add_constraint(MoveDown(TIMESTEP[AtTime]))
                AtTime += 1
            else:
                E.add_constraint(~MoveDown(TIMESTEP[AtTime]))
        elif orientation == "L":
            pass
        elif orientation == "R":
            pass
    
    # Move("U")
    Move("D")
    
    # we want to try move the tiles in a random direction at each timeStep
    # while AtTime < 16:
    #     Move(ORIENTATION[random.randint(0, 3)])
        
    print(GRID)
    
    
    # exactly one of the movement happens at a time and gives us a random object
    for timeStep in TIMESTEP:
        E.add_constraint(MoveUp(timeStep) | MoveDown(timeStep) | MoveLeft(timeStep) | MoveRight(timeStep) >> Random(RandomFill(), timeStep))
    
    
    # TODO if loc(x,y,t) and ORIENTATION(orientation, t) are true, then loc(x,y,t+1) is true
    # if we have location(x, y, t_i) and we move up, then we have location(x-1, y, t_(i+1))
    for timeStep in range(0, 15):
        for loc in LOCATION:
            if loc[0] != 1:
                E.add_constraint(Location(loc, TIMESTEP[timeStep]) & MoveUp(TIMESTEP[timeStep]) >> Location((loc[0] - 1, loc[1]), TIMESTEP[timeStep + 1]) & ~Location(loc, TIMESTEP[timeStep]))
    
    # if we have location(x, y, t_i) and we move down, then we have location(x+1, y, t_(i+1))
    for timeStep in range(0, 15):
        for loc in LOCATION:
            if loc[0] != 4:
                E.add_constraint(Location(loc, TIMESTEP[timeStep]) & MoveUp(TIMESTEP[timeStep]) >> Location((loc[0] + 1, loc[1]), TIMESTEP[timeStep + 1]) & ~Location(loc, TIMESTEP[timeStep]))
                
    # if we have location(x, y, t_i) and we move left, then we have location(x, y, t_(i+1))
    for timeStep in range(0, 15):
        for loc in LOCATION:
            if loc[1] != 1:
                E.add_constraint(Location(loc, TIMESTEP[timeStep]) & MoveUp(TIMESTEP[timeStep]) >> Location((loc[0], loc[1] - 1), TIMESTEP[timeStep + 1]) & ~Location(loc, TIMESTEP[timeStep]))
    
    # if we have location(x, y, t_i) and we move right, then we have location(x, y, t_(i+1))
    for timeStep in range(0, 15):
        for loc in LOCATION:
            if loc[1] != 4:
                E.add_constraint(Location(loc, TIMESTEP[timeStep]) & MoveUp(TIMESTEP[timeStep]) >> Location((loc[0], loc[1] + 1), TIMESTEP[timeStep + 1]) & ~Location(loc, TIMESTEP[timeStep]))
    
    
    # # Add custom constraints by creating formulas with the variables you created. 
    # E.add_constraint((a | b) & ~x)
    # # Implication
    # E.add_constraint(y >> z)
    # # Negate a formula
    # E.add_constraint(~(x & y))
    # # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    # constraint.add_exactly_one(E, a, b, c)

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    # T = T.compile()
    # print(T)
    # After compilation (and only after), you can check some of the properties
    # of your model:
    # print("\nSatisfiable: %s" % T.satisfiable())
    # print("# Solutions: %d" % count_solutions(T))
    # print("   Solution: %s" % T.solve())

    #E.introspect()
    
    # print("\nVariable likelihoods:")
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     # Ensure that you only send these functions NNF formulas
    #     # Literals are compiled to NNF here
    #     print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
