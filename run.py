
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

# adding all the possible locations to an array to store possible locations
LOCATION = []
for row in range(1, 5):
    for col in range(1, 5):
        LOCATION.append((row, col))
        
# an array of directions the tiles can move along
ORIENTATION = ['U', 'D', 'L', 'R']

# creates a 4x4 grid with all elements initialized to (0, 0), which represents an empty grid
for i in range(1, 5):
    GRID_COLS= []
    for j in range(1, 5):
        GRID_COLS.append((0, 0))
    GRID.append(GRID_COLS)

# function to generate tile on our grid
def GenerateTile(x, y):
    GRID[x - 1][y - 1] = (x,y)

print(GRID)

# the index representing the initial timestep
AtTime = 0
# boolean of our ability to move
move = False

# generates an array of possible timesteps from t_0 to t_15
TIMESTEP = []
for t in range(0, 16):
    TIMESTEP.append(f"t_{t}")
    
print(TIMESTEP)

# proposition to represent if there is a tile at a location at a certain timestep
@proposition(E)
class Location(object):
    def __init__(self, loc, timeStep):
        assert loc in LOCATION
        assert timeStep in TIMESTEP
        self.loc = loc
        self.timeStep = timeStep
    def _prop_name(self):
        return f"{self.loc} occupied @ {self.timeStep}"

# proposition to represent if a tile can move up at a certain timestep
@proposition(E)
class MoveUp(object):
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveUp @ {self.timeStep}"

# proposition to represent if a tile can move down at a certain timestep
@proposition(E)
class MoveDown(object):
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveDown @ {self.timeStep}"

# proposition to represent if a tile can move left at a certain timestep
@proposition(E)
class MoveLeft(object):
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveLeft @ {self.timeStep}"

# proposition to represent if a tile can move right at a certain timestep
@proposition(E)
class MoveRight(object):
    def __init__(self, timeStep):
        assert timeStep in TIMESTEP
        self.timeStep = timeStep
    def _prop_name(self):
        return f"moveRight @ {self.timeStep}"

# proposition to represent if a tile can move in a certain orientation at a certain timestep
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

# proposition to represent if a tile is randomly filled at a certain timestep
@proposition(E)
class Random(object):
    def __init__(self, loc, timeStep):
        assert loc in LOCATION
        assert timeStep in TIMESTEP
        self.loc = loc
        self.timeStep = timeStep
    def _prop_name(self):
        return f"{self.loc} randomly filled @ {self.timeStep}"
    
# test if a tile is at a location
def test_at_location(row, col):
    GenerateTile(row, col)
    E.add_constraint(~Location((row, col), 't_0'))

# fills a row and checks if tiles at that row can move in a certain orientation
# we would suggest you to test the first row and the last row (boundary rows)
def test_row_movement(row, orientation):
    for i in range(0,4):
        GRID[row - 1][i] = (row, i + 1)
        E.add_constraint(AbleToMove((row, i + 1), orientation, 't_0'))
        
# fills a column and checks if tiles at that column can move in a certain orientation
# we would suggest you to test the first column and the last column (boundary columns)
def test_col_movement(col, orientation):
    for i in range(0,4):
        GRID[i][col - 1] = (i+1, col)
        E.add_constraint(AbleToMove((i + 1, col), orientation, 't_0'))

# test if an empty grid can move (should not be able to move in any direction as there are no tiles)
def test_empty_grid_can_move():
    for row in range(0,4):
        for col in range(0,4):
            GenerateTile(0, 0)
    E.add_constraint(MoveUp('t_0'))
    E.add_constraint(MoveDown('t_0'))
    E.add_constraint(MoveLeft('t_0'))
    E.add_constraint(MoveRight('t_0'))


# the function where we will add all our constraints
def example_theory():
    
    # declare the global variables
    global AtTime
    global move
    
    # if location is not empty then there is a tile at that location
    for row in range(0,4):
        for col in range(0, 4):
            if GRID[row][col] != (0,0):
                E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]))
            elif GRID[row][col] == (0, 0):
                E.add_constraint(~Location((row + 1, col+ 1), TIMESTEP[AtTime]))
                
    # if a location does not have any tile, then that location cannot move in any direction (no tile existing)
    for row in range(0,4):
        for col in range(0, 4):
            if GRID[row][col] == (0,0):
                E.add_constraint(~Location((row + 1, col + 1), TIMESTEP[AtTime]) >> ~AbleToMove((row + 1, col + 1), 'U', TIMESTEP[AtTime]) &  ~AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]) &  ~AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]) &  ~AbleToMove((row + 1, col + 1), 'L', TIMESTEP[AtTime]))
                
    # a tile cannot move out of the grid
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
            
    # if a tile exists at a location and the location above that tile is empty, then the tile can move up to that location
    for row in range(0,4):
        for col in range(0,4):
            if row != 0 and GRID[row][col] == (row +1, col + 1) and GRID[row - 1][col] == (0,0):
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) & ~Location((row, col + 1), TIMESTEP[AtTime]) >> AbleToMove((row + 1, col + 1), 'U', TIMESTEP[AtTime]))
    
     # if a tile exists at a location and the location below that tile is empty, then the tile can move down to that location
    for row in range(0,4):
        for col in range(0,4):
            if row != 3 and GRID[row][col] == (row +1, col + 1)  and GRID[row + 1][col] == (0,0):
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) & ~Location((row + 2, col + 1), TIMESTEP[AtTime]) >> AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]))
            

    # if a tile exists at a location and the location to the left of that tile is empty, then the tile can move left to that location
    for row in range(0,4):
        for col in range(0,4):
            if col != 0 and GRID[row][col] == (row +1, col + 1) and GRID[row][col - 1] == (0,0):
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) & ~Location((row + 1, col), TIMESTEP[AtTime]) >> AbleToMove((row + 1, col + 1), 'L', TIMESTEP[AtTime]))
  
    # if a tile exists at a location and the location to the right of that tile is empty, then the tile can move right to that location
    for row in range(0,4):
        for col in range(0,4):
            if col != 3 and GRID[row][col] == (row +1, col + 1) and GRID[row][col + 1] == (0,0):
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) & ~Location((row + 1, col + 2), TIMESTEP[AtTime]) >> AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]))
                
    
    # picks a random orientation for the constraints below
    r_int = random.randint(0,3)
    Orientation = ORIENTATION[r_int]
    
    # at least one tile is able to move in a certain direction, movement in that direction should be possible
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
    
    # recurive function to move the tiles up in the grid
    def UpMove(x,y):
        if x == 0 or GRID[x-1][y] != (0, 0):
            return 
        if GRID[x][y] != (0,0):
            # move the tile up and update its coordinates (only updates the x coordinate)
            GRID[x-1][y] = (x, GRID[x][y][1]) 
            GRID[x][y] = (0, 0)
            UpMove(x - 1, y)   
    
    # recurive function to move the tiles down in the grid         
    def DownMove(x,y):
        if x == 3 or GRID[x+1][y] != (0, 0):
            return
        
        if GRID[x][y] != (0, 0):
            # move the tile down and update its coordinates (only updates the x coordinate)
            GRID[x+1][y] = (x+2, GRID[x][y][1]) 
            GRID[x][y] = (0, 0)

            DownMove(x + 1, y) 
    
    # recurive function to move the tiles left in the grid        
    def LeftMove(x,y):
        if y == 0 or GRID[x][y-1] != (0, 0):
            return
        
        if GRID[x][y] != (0, 0):
            # move the tile left and update its coordinates (only updates the y coordinate)
            GRID[x][y-1] = (GRID[x][y][0], y) 
            GRID[x][y] = (0, 0)

            LeftMove(x, y - 1) 
    
    # recurive function to move the tiles right in the grid
    def RightMove(x,y):
        if y == 3 or GRID[x][y+1] != (0, 0):
            return
        
        if GRID[x][y] != (0, 0):
            # move the tile right and update its coordinates (only updates the y coordinate)
            GRID[x][y+1] = (GRID[x][y][0], y+2) 
            GRID[x][y] = (0, 0)

            RightMove(x, y + 1)
    
    # recurive function to calculate the distance a tile can move up in the grid
    def DistanceUp(x, y):
        if x == 0 or GRID[x-1][y] != (0, 0):
            return 0

        else: 
            return 1 + DistanceUp(x - 1, y)
    
    # recurive function to calculate the distance a tile can move down in the grid
    def DistanceDown(x, y):
        if x == 3 or GRID[x+1][y] != (0, 0):
            return 0

        else: 
            return 1 + DistanceDown(x + 1, y)
    
    # recurive function to calculate the distance a tile can move left in the grid
    def DistanceLeft(x, y):
        if y == 0 or GRID[x][y-1] != (0, 0):
            return 0

        else: 
            return 1 + DistanceLeft(x, y - 1)
    
    # recurive function to calculate the distance a tile can move right in the grid
    def DistanceRight(x, y):
        if y == 3 or GRID[x][y+1] != (0, 0):
            return 0
        else: 
            return 1 + DistanceRight(x, y + 1)
    
        
    GridTemp = copy.deepcopy(GRID)  
    
    # if a tile is at a location and it is able to move down, and our grid has moved down, then the tile should move down as far as possible
    if Orientation == 'D':
        row = 3       
        while  row > -1:
            for col in range(0, 4):
                if row != 3 and GRID[row][col] != (0,0) and GRID[row + 1][col] == (0,0):
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'D', TIMESTEP[AtTime]) & MoveDown(TIMESTEP[AtTime]) >> Location((row + 1 + DistanceDown(row, col) , col + 1), TIMESTEP[AtTime + 1]))
                    DownMove(row, col) 
            row -= 1
    # if a tile is at a location and it is able to move right, and our grid has moved right, then the tile should move right as far as possible
    elif Orientation == 'R':
        for row in range(0,4):
            col = 3  
            while col > - 1:
                if col != 3 and GRID[row][col] != (0,0) and GRID[row][col + 1] == (0,0):
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'R', TIMESTEP[AtTime]) & MoveRight(TIMESTEP[AtTime]) >> Location((row + 1 , col + 1 + DistanceRight(row, col)), TIMESTEP[AtTime + 1]))
                    RightMove(row, col) 
                col -= 1
    
    # if a tile is at a location and it is able to move up, and our grid has moved up, then the tile should move up as far as possible        
    for row in range(0,4):
        for col in range(0,4):
                if row != 0 and GRID[row][col] != (0,0) and GRID[row - 1][col] == (0,0) and Orientation == 'U':
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'U', TIMESTEP[AtTime]) & MoveUp(TIMESTEP[AtTime]) >> Location((row + 1 - DistanceUp(row, col) , col + 1), TIMESTEP[AtTime + 1]))
                    # print(TIMESTEP[AtTime])
                    UpMove(row, col)
                   
                # if a tile is at a location and it is able to move left, and our grid has moved left, then the tile should move left as far as possible   
                elif col != 0 and GRID[row][col] != (0,0) and GRID[row][col - 1] == (0,0) and Orientation == 'L':
                    move = True
                    E.add_constraint(Location((row + 1, col+ 1), TIMESTEP[AtTime]) & AbleToMove((row + 1, col + 1), 'L', TIMESTEP[AtTime]) & MoveLeft(TIMESTEP[AtTime]) >> Location((row + 1 , col + 1 - DistanceLeft(row, col)), TIMESTEP[AtTime + 1]))
                    LeftMove(row, col)
    
    # creates a random tile at an empty location
    def RandomFill():
        # we want to randomly fill a location that is empty
        emptyloc = []
        for row in range(0,4):
            for col in range(0,4):
                if GRID[row][col] == (0,0):
                    emptyloc.append((row + 1, col + 1))
        randomLoc = random.choice(emptyloc)
        GRID[randomLoc[0]-1][randomLoc[1]-1] = randomLoc
        return randomLoc   
    
    # if the grid has not changed, then we cannot move in that direction    
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
    # if the grid has changed, we randomly fill a location
    else:
        randomloc = RandomFill()
        # random tile generated at a location only if that location does not have a tile on it
        E.add_constraint(~Location(randomloc, TIMESTEP[AtTime]) >> Random(randomloc, TIMESTEP[AtTime + 1]))
    
    
    #  ff a location has a tile on it then a random tile cannot be placed at that location
    for row in range(0,4):
        for col in range(0,4):
            if GRID[row][col] != (0,0) and AtTime < 15:
                E.add_constraint(Location((row + 1, col + 1), TIMESTEP[AtTime]) >> ~Random((row + 1, col + 1), TIMESTEP[AtTime + 1]))
  
    return E


if __name__ == "__main__":

    """
    uncomment the following lines below only when you want to use the above test functions
    
    T = example_theory()
    
    test_at_location(3,1) 
    test_row_movement(1, 'D') # you can test whatever row number and orientation you want
    test_col_movement(2, 'L') # you can test whatever column number and orientation you want
    test_random(2,2) 
    test_empty_grid_can_move()
    
    T = T.compile()
    S = T.solve()
    print(S)
    """
    
    GenerateTile(4, 2) # this will generate a grid with a tile at location (4, 2), you can initialize the grid with whatever first tile you want
    # print(GRID)
    
    # function to run the 2048 simulation
    def run_2048_simulation():
        
        global AtTime
        
        # loop to run the simulation for 15 timesteps
        while AtTime < 15:
            # if move in any orientation has been made, we increment the timestep         
            if move == True: 
                AtTime += 1  
                
            T = example_theory()
            T = T.compile()
            
            # print(T)
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
                        
                if s and AtTime < 15:       
                    print(f"\n\n Our Grid updated: {GRID} ")                  
            else:
                print('No Solution')

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
