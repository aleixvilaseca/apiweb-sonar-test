
import math

# defining a function for round down.
def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

# define a function for round_up
def round_up(n, decimals = 0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier