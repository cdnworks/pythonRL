from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

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
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov() # Update the play'ers FOV before their next action

    def update_fov(self) -> None:
        '''
        Recompute the visible area based on the player's point of view
        '''
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=8
        )
        # If a tile is 'visible', it should be added to 'explored'
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            # Print entities that are in the FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()