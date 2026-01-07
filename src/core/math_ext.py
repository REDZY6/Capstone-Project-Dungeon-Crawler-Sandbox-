from math import sqrt

def distance(x, y, other_x, other_y):
    # Pythagoras theorum to calculate the distance with player and sprite
    return sqrt((other_x - x)**2 + (other_y - y)**2)