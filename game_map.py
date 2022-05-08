from __future__ import annotations
import numpy as np  # type: ignore
from tcod.console import Console
import tcod
import random
import global_vars


from typing import Iterable, TYPE_CHECKING

import tile_types


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height



    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
