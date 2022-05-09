from typing import Tuple

from game_map import GameMap
import tile_types
from typing import Iterator, List, Tuple, TYPE_CHECKING
import random
import tcod
import entity_factories
import global_vars
import numpy as np

from engine import Engine

if TYPE_CHECKING:
    from engine import Engine


class Building:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.y1, self.y2), slice(self.x1, self.x2)

    def intersects(self, other) -> bool:
        """Return True if this overlaps with another thing."""
        #return (
            #(
            #self.x1 <= other.x2
            #and self.x2 >= other.x1
            #and self.y1 <= other.y2
            #and self.y2 >= other.y1
            #)
        #)
        if (self.x1>=other.x2) or (self.x2<=other.x1) or (self.y2<=other.y1) or (self.y1>=other.y2):
            return False
        else:
            return True

class Road:
    def __init__(self, x_root: int, y_root: int, x_goal: int, y_goal: int, width: int):
        
        x_width=False
        y_width=True
        odd_width=False
        if x_root==x_goal:
            x_width=True
            y_width=False
        if width%2==0:
            odd_width=True
        x1_mod = int(width/2)*x_width
        x2_mod = (int(width/2)+odd_width)*x_width
        y1_mod = int(width/2)*y_width
        y2_mod = (int(width/2)+odd_width)*y_width
        self.x1 = min(x_root,x_goal)-x1_mod
        self.y1 = min(y_root,y_goal)-y1_mod
        self.x2 = max(x_root,x_goal)+x2_mod+1
        self.y2 = max(y_root,y_goal)+y2_mod+1

    @property
    def area(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1, self.x2),slice(self.y1, self.y2)
    
    def intersects(self, other) -> bool:

        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2 
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def place_entities(
    room: Road, city: GameMap,
) -> None:
    number_of_police = 1
    for i in range(number_of_police):
        x = random.randint(room.x1, room.x2-1)
        y = random.randint(room.y1, room.y2-1) 
        if not any(entity.x == x and entity.y == y for entity in city.entities):
            entity_factories.police.spawn(city, x, y)


def generate_city(map_width, map_height, engine: Engine) -> GameMap:

    player = engine.player
    city = GameMap(engine, map_width, map_height, entities=[player])

    roads: List[Road] = []
    buildings: List[Building] = []
    roads = generate_roads(map_width, map_height)
    for road in roads:
        city.tiles[road.area] = tile_types.road
    
    # The road we'll spawn the player on, we won't spawn police there.
    player_road_reference = random.randint(0,len(roads)-1)

    for i in range(global_vars.number_police):
        if i==0:
            player_road = roads[player_road_reference]
            x = random.randint(player_road.x1, player_road.x2-1)
            y = random.randint(player_road.y1, player_road.y2-1)
            player.place(x, y, city) 
        
        police_road_reference = player_road_reference
        road = roads[police_road_reference]
        while police_road_reference == player_road_reference:
            police_road_reference = random.randint(0,len(roads)-1)
            road = roads[police_road_reference]
        place_entities(road, city)

    # Generate buildings
    number_buildings = random.randrange(global_vars.min_number_buildings,global_vars.max_number_buildings)
    for tag in range(number_buildings):
        while(True):
            #determine size and location
            size_x = random.randrange(global_vars.min_building_edge,global_vars.max_building_edge)
            size_y = random.randrange(max(global_vars.min_building_edge,size_x-global_vars.max_building_edge_range),min(global_vars.max_building_edge,size_x+global_vars.max_building_edge_range))
            root_x = random.randrange(0, map_width+1-size_x)
            root_y = random.randrange(0, map_height+1-size_y)

            new_building = Building(x=root_x, y=root_y, width=size_x, height=size_y)

            all_items = []
            all_items= np.concatenate((buildings, roads))



            if not any(new_building.intersects(map_item) for map_item in all_items):
                buildings.append(new_building)
                for i in range(new_building.x1,new_building.x2):
                    for j in range(new_building.y1,new_building.y2):
                        city.tiles[i][j] = tile_types.new_building_tile(size=size_x*size_y, tag=tag)
                break

    return city

def generate_roads(width, height):
    while True:
        points = [[0 for i in range(height)] for j in range(width)]
        unaccessible = []
        accessable =[]
        roads=[]
        
        # Number of points of interest, roads need to connect through these
        vertical_roads_number = random.randrange(2,5) # Top to bottom connections
        horizontal_roads_number = random.randrange(2,5) #L/R connections
        intersections = random.randrange(15,25)

        # Add points of interest to the graph
        for x in range(vertical_roads_number):
            crossing = random.randrange(5,width-5)
            points[crossing][0] = 1
            points[crossing][height-1] = 1
            unaccessible.append([crossing,height-1])
            unaccessible.append([crossing,0])
        for x in range(horizontal_roads_number):
            crossing = random.randrange(5,height-5)
            points[0][crossing] = 1
            points[width-1][crossing] = 1
            unaccessible.append([width-1,crossing])
            unaccessible.append([0,crossing])
        for x in range(intersections):
            crossing_x = random.randrange(5,width-5)
            crossing_y = random.randrange(5,height-5)
            points[crossing_x][crossing_y] = 1
            unaccessible.append([crossing_x,crossing_y])

        
        key_unaccessible = unaccessible[random.randrange(0,len(unaccessible)-1)]
        accessable.append(key_unaccessible)
        unaccessible.remove(key_unaccessible)

        # We have a list, unaccessible, and a root node
        while True: 
            # Evaluate all points
            for goal in unaccessible:
                graph = tcod.path.SimpleGraph(cost=points, cardinal=1, diagonal=0)
                pf = tcod.path.Pathfinder(graph)
                pf.add_root(key_unaccessible)
                if len(pf.path_from(goal)) > 2:
                    #Update arrays
                    unaccessible.remove(goal)
                    accessable.append(goal)
            
            # Pick a point and pull it in    
            if (len(unaccessible) != 0):
                # Get a root and goal (randomly choosing from available and unavailable points)
                goal = unaccessible[random.randrange(0,len(unaccessible))]
                root = accessable[random.randrange(0,len(accessable))]
                # Generate a corner, a road to the corner from the root, and from corner to goal
                corner = road_corner(root, goal)

                roads.append(Road(x_root=root[0], y_root=root[1], x_goal=corner[0], y_goal=corner[1], width=1))
                roads.append(Road(x_root=corner[0], y_root=corner[1], x_goal=goal[0], y_goal=goal[1], width=1))
                
                # Get the points between so you may update the arrays with what exists
                for x, y in road_between(root, goal, corner):
                    #Update arrays
                    #TODO: This should have the width added to it, here or in road between
                    points[x][y] = 1
                    accessable.append((x,y))
            else:
                return roads

        return roads

def road_corner(
       start: Tuple[int, int], end: Tuple[int, int]
) -> Tuple[int, int]:
   """Return an L-shaped tunnel between these two points."""
   x1, y1 = start
   x2, y2 = end
   if random.random() < 0.5:  # 50% chance.
       # Move horizontally, then vertically.
       return [x2, y1]
   else:
       # Move vertically, then horizontally.
       return [x1, y2] 

def road_between(
   start: Tuple[int, int], end: Tuple[int, int], corner: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    #TODO: Add width
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = corner
    x3, y3 = end

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (x2, y2)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((x2, y2), (x3, y3)).tolist():
        yield x, y