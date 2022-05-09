from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor

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
