import numpy as np  # type: ignore
from tcod.console import Console
import tcod
import random
from typing import Iterator, Tuple
import global_vars


import tile_types


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        self.setup_taken=generate_roads(width, height)
        # Populate roads
        i=0
        for row in self.setup_taken:
            j= 0
            for item in row:
                if item == 1:
                    self.tiles[j][i] = tile_types.road
                j+=1
            i+=1
        self.generate_buildings()


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height



    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
    
    def generate_buildings(self):
        number_buildings = random.randrange(300,500)
        for tag in range(number_buildings):

            size_x = random.randrange(global_vars.min_building_edge,global_vars.max_building_edge)
            size_y = random.randrange(max(global_vars.min_building_edge,size_x-global_vars.max_building_edge_range),min(global_vars.max_building_edge,size_x+global_vars.max_building_edge_range))
            root_x = random.randrange(size_x, self.width-1-size_x)
            root_y = random.randrange(size_y, self.height-1-size_y)

            if check_building(self.setup_taken, root_x, root_y, size_x, size_y):
                spacing = random.randrange(0,2)
                self.mark_building(root_x, root_y, size_x, size_y, spacing)
                self.build_building(root_x=root_x, root_y=root_y, size_x=size_x, size_y=size_y, tag=tag)
                                    
                


    # Assume you have planning permission
    def build_building(self, root_x: int, root_y: int, size_x: int, size_y: int, tag:int):
        for i in range(size_x):
            for j in range(size_y):
                print("placing",root_x-1+i," ",root_y-1+j) 
                self.tiles[root_x-1+i][root_y-1+j] = tile_types.new_building_tile(size=size_x*size_y, tag=tag)

    def mark_building(self, root_x, root_y, size_x, size_y, spacing):
        print("root_x",root_x,"root_y",root_y,"size_x",size_x,"size_y",size_y,"spacing",spacing)
        for i in range(size_x+(spacing*2)):
            for j in range(size_y+(spacing*2)):
                
                x=root_x-spacing+i-1
                y=root_y-spacing+j-1
                print("marking",y," ",x)
                if self.setup_taken[y][x] ==0:
                    print("reallymarking",y," ",x) 
                    self.setup_taken[y][x] = 1

# [Top0/Bottom][L0/R]
def generate_roads(width, height):
    while True:
        points = [[0 for i in range(width)] for j in range(height)]
        unaccessable = []
        accessable =[]
        
        # Number of points of interest, roads need to connect through these
        vertical_roads_number = random.randrange(1,4) # Top to bottom connections
        horizontal_roads_number = random.randrange(1,4) #L/R connections
        intersections = random.randrange(10,20)

        # Add points of interest to the graph
        for x in range(vertical_roads_number):
            crossing = random.randrange(5,width-5)
            points[0][crossing] = 1
            points[height-1][crossing] = 1
            unaccessable.append([height-1,crossing])
            unaccessable.append([0,crossing])
        for x in range(horizontal_roads_number):
            crossing = random.randrange(5,height-5)
            points[crossing][0] = 1
            points[crossing][width-1] = 1
            unaccessable.append([crossing,width-1])
            unaccessable.append([crossing,0])
        for x in range(intersections):
            crossing_x = random.randrange(5,width-5)
            crossing_y = random.randrange(5,height-5)
            points[crossing_y][crossing_x] = 1
            unaccessable.append([crossing_y,crossing_x])

        
        key_unaccessable = unaccessable[random.randrange(0,len(unaccessable)-1)]
        accessable.append(key_unaccessable)
        unaccessable.remove(key_unaccessable)

        # We have a list, unaccessable, and a root node
        while True: #TODO: swap back
            # Evaluate all points
            for goal in unaccessable:
                graph = tcod.path.SimpleGraph(cost=points, cardinal=1, diagonal=0)
                pf = tcod.path.Pathfinder(graph)
                pf.add_root(key_unaccessable)
                if len(pf.path_from(goal)) > 2:
                    #Update arrays
                    unaccessable.remove(goal)
                    accessable.append(goal)
            
            # Pick a point and pull it in    
            if (len(unaccessable) != 0):
                goal = unaccessable[random.randrange(0,len(unaccessable))]
                root = accessable[random.randrange(0,len(accessable))]
                for x, y in tunnel_between(root, goal):
                    #Update arrays
                    points[x][y] = 1
                    accessable.append((x,y))
            else:
                return points
        return points

def tunnel_between(
   start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
   """Return an L-shaped tunnel between these two points."""
   x1, y1 = start
   x2, y2 = end
   if random.random() < 0.5:  # 50% chance.
       # Move horizontally, then vertically.
       corner_x, corner_y = x2, y1
   else:
       # Move vertically, then horizontally.
       corner_x, corner_y = x1, y2

   # Generate the coordinates for this tunnel.
   for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
       yield x, y
   for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
       yield x, y


def check_building(space, root_x, root_y, size_x, size_y):
    for i in range(size_x):
        for j in range(size_y):
            if space[root_y+j-1][root_x+i-1] > 0:
                print("false check")
                return False        
    print("true check")    
    return True

