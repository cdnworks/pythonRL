#!/usr/bin/env python3
import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


def main() -> None:
    # Screen/Console params
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    # Initialize some basic entities
    player = Entity(int(screen_width/2), int(screen_height/2), '@', 
        (255, 255, 255))
    test_npc = Entity(int(screen_width/2 + 5), int(screen_height/2 - 5), '@', 
        (255, 255, 0))
    entities = {test_npc, player}

    # Initialize game map
    game_map = GameMap(map_width, map_height)

    # Initialize the game engine
    engine = Engine(entities=entities, event_handler=event_handler, 
        game_map=game_map, player=player)
    

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Sludge Rogue",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")

        # Game loop
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()