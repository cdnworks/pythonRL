#!/usr/bin/env python3
import copy

import tcod

from engine import Engine
from entity import Entity
import entity_factories
from input_handlers import EventHandler
from procgen import generate_dungeon


def main() -> None:
    # Screen/Console params
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    # Procgen params
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # Mobgen params
    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    # Initialize some basic entities
    player = copy.deepcopy(entity_factories.player)

    # Initialize game map
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        player=player
    )

    # Initialize the game engine
    engine = Engine(event_handler=event_handler, game_map=game_map, 
        player=player)
    

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