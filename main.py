#!/usr/bin/env python3
import tcod
import copy
from engine import Engine
import entity_factories
from procgen import generate_city
from input_handlers import EventHandler


def main() -> None:
    screen_width = 210
    screen_height = 75

    map_width = 200
    map_height = 70

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = copy.deepcopy(entity_factories.player)

    game_map = generate_city(map_width, map_height, player)

    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="FLCL inspired proof of concept",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()
