#!/usr/bin/env python3
import copy
import traceback

import tcod

import color
from engine import Engine
import entity_factories
from procgen import generate_dungeon


def main() -> None:
    # Screen/Console params
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    # Procgen params
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # Mobgen params
    max_monsters_per_room = 2

    # Itemgen params
    max_items_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # Initialize some basic entities
    player = copy.deepcopy(entity_factories.player)
    
    # Initialize the game engine
    engine = Engine(player=player)

    # Initialize game map
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        max_items_per_room=max_items_per_room,
        engine=engine
    )

    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", 
        color.welcome_text
    )

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
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception: # Exception handler
                traceback.print_exc() # Print exception to stderr
                # Then print the error to message log
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
    main()