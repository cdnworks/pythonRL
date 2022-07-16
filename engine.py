from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    '''
    Class responsible for making the appropriate calls in response to game
    events and actions, and rendering the screen on a tcod console
    '''
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, 
        game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        # While the player is an entity itself, its not in the set
        # for ease of access later on since we do more things to/with the player
        # than any other entity
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()