#!/usr/bin/env python3
import tcod
import copy
from engine import Engine
import entity_factories
from procgen import generate_city
from input_handlers import EventHandler
import global_vars


def main() -> None:

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map = generate_city(global_vars.map_width, global_vars.map_height, engine=engine)


    with tcod.context.new_terminal(
        global_vars.screen_width,
        global_vars.screen_height,
        tileset=tileset,
        title="FLCL inspired proof of concept",
        vsync=True,
    ) as context:
        root_console = tcod.Console(global_vars.screen_width, global_vars.screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
