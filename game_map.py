from __future__ import annotations
import numpy as np  # type: ignore
from tcod.console import Console
import tcod
import random
import global_vars


from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import tile_types

from entity import Actor

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int,
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity

        return None
    
    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height



    def render(self, console: Console) -> None:

        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            if entity.tile:
                console.print(
                        x=entity.x, y=entity.y, string=entity.char, bg=entity.color
                    )
            else:
                console.print(
                        x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                    )
