
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
import random

# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding

# empty 2D array to represent the grid
GRID = []

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
TIME = 0
print(f"t_{TIME}")

LOCATION = []
for row in range(1, 5):
    for col in range(1, 5):
        LOCATION.append((row, col))
        
ORIENTATION = ['U', 'D', 'L', 'R']

@proposition(E)
class Location:
    def __init__(self, loc, time):
        assert loc in LOCATION
        assert time in range(0, 17)
        self.loc = loc
        self.time = time
    def _prop_name(self):
        return f"{self.loc} is occupied @ step {self.time}"

@proposition(E)
class ORIENTATION:
    def __init__(self, orientation):
        assert orientation in ORIENTATION
        self.orientation = orientation
    def _prop_name(self):
        return f"{self.orientation}"
    
# we want to start the grid with a random location (x, y) being filled 
# 


# TODO make able_to_move of a tuple (x, y) at timestep t a constraint from recursion

# TODO timestep cannot go back  is a constraint

# TODO loc(x,y,t) cannot be both true and false

# TODO create a constraint moveup(t) that takes in a timestep and returns true if the player has moved at that timestep

# TODO if loc(x,y,t) and moveup(t) are true, then loc(x,y,t+1) is true

# TODO randomly fill one location that is empty (i.e. not in the array GRID) and then update GRID



@proposition(E)
class BasicPropositions:    

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"{self.data}"

@proposition(E)
class Tile:
    def __init__(self, name, value):
        assert value in TILE_VALUES
        assert name in TILE_NAMES
        self.name = name
        self.value = value
    def _prop_name(self):
        return f"{self.name}: {self.value}"
    def __str__(self):
        return f"{self.name}: {self.value}"
    
class Location:
    def __init__(self, tile, loc):
        assert tile in TILES
        assert loc in LOCATION
        self.loc = loc
        self.tile = tile
    def _prop_name(self):
        return f"{self.tile} @ {self.loc}"


GRID = []
TILES = []

for i in range(1, 5):
    for j in range(1,5):
        TILES.append(Tile(f'{i}{j}', ''))
# Generate grid
for i in range(1, 5):
    GRID_COLS= []
    for j in range(1, 5):
        GRID_COLS.append(Tile(f'{row}{col}', ''))
    GRID.append(GRID_COLS)
    
# Randomly give two tiles value of 2  
for r in range(0, 2):
    row = random.randint(1, 4)
    col = random.randint(1, 4)
    while row == col:
        row = random.randint(1, 4)
    GRID[row][col] = Tile(f'{row + 1}{col + 1}', 2)
    


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

# Call your variables whatever you want
a = BasicPropositions("a")
b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    
    # For every location at most on tile
    for location in LOCATION:
        tile_props = []
        for tile in TILES:
            tile_props.append(Location(tile, location))
        constraint.add_exactly_one(E, tile_props)
        
        
    # Add custom constraints by creating formulas with the variables you created. 
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
