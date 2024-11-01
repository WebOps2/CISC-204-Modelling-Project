
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
import random

# Encoding that will store all of your constraints
E = Encoding()

# TILES = []
LOCATIONS = []
LOCATIONS_GRID = {}
ORIENTATIONS = list('UDLR')

def gen_locations(rows, cols):
    assert rows == 4, "Our board is a 4 X 4 grid"
    assert cols == 4, "Our board is a 4 X 4 grid"
    for row in range(1,rows + 1):
        LOCATIONS_GRID[row] = {}
        for col in range(1, cols+1):
            LOCATIONS.append(f'{row}{col}')
            LOCATIONS_GRID[row][col] = f'{row}{col}'
            
def gen_tiles(rows, cols):
    assert rows == 4, "Our board is a 4 X 4 grid"
    assert cols == 4, "Our board is a 4 X 4 grid"
    for row in range(1,rows + 1):
        for col in range(1, cols+1):
            TILES.append(f"t{row}{col}")

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:    

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"

@proposition(E)
@proposition(E)
class Tiles:
    def __init__(self, value, loc):
        assert loc in LOCATIONS
        self.loc = loc
        self.value = value
    
    
@proposition(E)
class Location:
    def __init__(self, tile, loc):
        assert loc in LOCATIONS
        assert tile in TILES
        self.tile = tile
        self.loc = loc
    def _prop_name(self):
        return f"({self.tile} @ {self.loc})"
    
    
@proposition(E)
class EmptyTile:
    def __init__(self, tile, loc):
        assert loc in LOCATIONS
        assert tile in TILES
        self.tile = tile
        self.loc = loc
        
    def _prop_name(self):
        return f"({self.tile} is empty @ location {self.loc})"

@proposition(E)
class CanMerge:
    def __init__(self, tile, o):
        assert tile in TILES
        assert o in ORIENTATIONS
        self.tile = tile
        self.o = self.o


@proposition(E)        
class NextTile:
    def __init__(self,tile, o):
        assert tile in TILES
        assert o in ORIENTATIONS
        self.tile = tile
        self.o = o

random_val1 = random.randint(0, len(LOCATIONS))
random_val2 = random.randint(0, len(LOCATIONS))

TILES = [Tiles(2, LOCATIONS[random_val1]), Tiles(2, LOCATIONS[random_val2])]

for location in LOCATIONS:
    tile_at_props = []
    for tile in TILES:
        tile_at_props.append(Location(tile, location))
    constraint.add_at_most_one(E, tile_at_props)

for location in LOCATIONS:
    location_at_props = []
    for tile in TILES:
        if tile.loc != location:
            location_at_props.append(Location(tile, location))
    constraint.add_at_most_one(E, location_at_props)
    

        



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
