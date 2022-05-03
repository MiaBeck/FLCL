from typing import Tuple

import numpy as np  # type: ignore
import utils

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
        ("building_tag", int), #To tell buildings apart
    ]
)



def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    building_tag: int,
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light, building_tag), dtype=tile_dt)

def new_building_tile(*, size: int, tag: int) -> np.ndarray:
    colour = utils.building_colour(size)
    light = (ord(" "), (colour, colour, colour), (colour, colour, colour))

    return np.array((False, False, light, light, tag), dtype=tile_dt)

road = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (100, 75, 80), (100, 75, 80)),
    light=(ord(" "), (100, 75, 80), (100, 75, 80)),
    building_tag=0,
)
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
    building_tag=0,
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
    building_tag=0,
)

