from typing import Tuple


class Entity:
    '''
    Generic object to represent in-game objects/actors.
    i.e. players, enemies, items, etc
    '''

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        # color is a tuple of 3 integers representing a RGB value
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        # Some entities can move, like enemies or the player.
        self.x += dx
        self.y += dy
