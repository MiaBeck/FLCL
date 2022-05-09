from components.ai import HostileEnemy, BuildingAI
from components.fighter import Fighter
from entity import Actor
from utils import building_colour

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
)

police = Actor(
    char="P",
    color=(15, 82, 186),
    name="Police", 
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
)

#TODO: Tag
def building(tag:int, size: int):
    colour=building_colour(size)
    return Actor(
    char=" ",
    color=(colour, colour, colour),
    tile=True,
    name="Building",
    ai_cls=BuildingAI,
    fighter=Fighter(hp=30, defense=2, power=5),
    )

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
)