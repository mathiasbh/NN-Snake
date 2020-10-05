from segment import Segment
from random import randrange
from numpy import pi, cos, sin, arctan2, concatenate

class Snake(object):
    """docstring for Snake"""
    def __init__(self, x, y, len, off):
        self.x = x
        self.y = y
        self.len = len
        self.off = off
        self.dir = pi/2 * randrange(4)
        self.segments = [Segment(self.x, self.y, self.len)]
        self.segments.append(Segment(self.x, self.y, self.len))
        self.segments.append(Segment(self.x, self.y, self.len))


    def update_pos(self):
        """
            Update position of snake including all segments.
        """
        for s in range(len(self.segments), 1, -1):
            self.segments[s-1].update_pos(self.segments[s - 2].x, self.segments[s - 2].y)

        self.x += int(round(cos(self.dir))) * self.len
        self.y += int(round(sin(self.dir))) * self.len

        self.segments[0].update_pos(self.x, self.y)



    def update_dir(self, dir):
        """
            Update direction of snake. Simple controls of left/right turns.
        """
        directions = {'lt' : pi/2.0,
                      'rt' : -pi/2.0}

        if (dir == 'lt'):  # Left turn
            self.dir += directions[dir]
        elif (dir == 'rt'):  # Right turn
            self.dir += directions[dir]
        else:
            pass

        self.dir = self.dir % (2.0 * pi)


    def add_segment(self, x, y, len):
        self.segments.append(Segment(self.x, self.y, self.len))


    def collision_wall(self, wall, off, width, height):
        return((self.x - self.len < off) | (self.x > width - off) | (self.y - self.len < off) | (self.y > height - off))
    


    def collision_snake(self):
        """
            Determine collision between snake and snake segments.
        """
        collide = False
        for s in range(1, len(self.segments)):
            if ((self.x == self.segments[s].x) & (self.y == self.segments[s].y)):
                collide = True
        return(collide)


    def collision_point(self, point):
        """
            Determine collision between snake and food/point.
        """
        return((self.x == point.x) & (self.y == point.y))


    def nearst_wall(self, walls, width, height):
        """
            Finds distance to nearest wall or snake segment.
            Allows randomly placed walls - surely, there's a better way :)
        """
        ndistance = 1 # North
        edistance = 1 # East
        sdistance = 1 # South
        wdistance = 1 # West
  
        for wall in walls:
            # NORTH
            if (self.x >= wall.a[0]) and (self.x <= wall.b[0]):
                if ((wall.a[1] - self.y)/height < ndistance) and (wall.a[1] - self.y) > 0:
                    ndistance = (wall.a[1] - self.y - self.len/2)/height
            # SOUTH
            if (self.x >= wall.a[0]) and (self.x <= wall.b[0]):
                if ((self.y - wall.a[1])/height < sdistance) and (self.y - wall.a[1]) > 0:
                    sdistance = (self.y - wall.a[1] - self.len)/height

            # EAST
            if (self.y >= wall.a[1]) and (self.y <= wall.b[1]):
                if ((wall.a[0] - self.x)/width < edistance) and (wall.a[0] - self.x) > 0:
                    edistance = (wall.a[0] - self.x - self.len/2)/width

            # WEST
            if (self.y >= wall.a[1]) and (self.y <= wall.b[1]):
                if ((self.x - wall.a[0])/width < wdistance) and (self.x - wall.a[0]) > 0:
                    wdistance = (self.x - wall.a[0] - self.len)/width
      
      
        for segment in self.segments:
            # NORTH
            if (self.x == segment.x) and (segment.y > self.y) and ((segment.y - self.y)/height < ndistance):
                ndistance = (segment.y - self.y)/height
            
            # SOUTH
            if (self.x == segment.x) and (self.y > segment.y) and ((self.y - segment.y)/height < sdistance):
                sdistance = (self.y - segment.y)/height
            
            # EAST
            if (self.y == segment.y) and (segment.x > self.x) and ((segment.x - self.x)/width < edistance):
                edistance = (segment.x - self.x)/width
            
            # WEST
            if (self.y == segment.y) and (self.x > segment.x) and ((self.x - segment.x)/width < wdistance):
                wdistance = (self.x - segment.x)/width


        if self.dir == pi/2 * 0: # East
            return([ndistance, edistance, sdistance])
        elif self.dir == pi/2 * 1: # North
            return([wdistance, ndistance, edistance])
        elif self.dir == pi/2 * 2: # West
            return([sdistance, wdistance, ndistance])
        elif self.dir == pi/2 * 3: # South
            return([edistance, sdistance, wdistance])
        else:
            return([None,None,None])
        
        
    def simple_nearest_wall(self, walls, pxsize):
        """
            Finds boolean value of nearest wall or snake segment.
        """
        ndistance = 0 # North
        edistance = 0 # East
        sdistance = 0 # South
        wdistance = 0 # West
        
  
        for wall in walls:
            # NORTH
            if (self.x >= wall.a[0]) and (self.x <= wall.b[0]) and ((wall.b[1] - self.y - self.len/2) == 0):
                ndistance = 1
            # SOUTH
            if (self.x >= wall.a[0]) and (self.x <= wall.b[0]) and ((self.y - wall.b[1] - self.len) == 0):
                sdistance = 1
            # EAST
            if (self.y >= wall.a[1]) and (self.y <= wall.b[1]) and ((wall.b[0] - self.x - self.len/2) == 0):
                edistance = 1
            # WEST
            if (self.y >= wall.a[1]) and (self.y <= wall.b[1]) and ((self.x - wall.b[0] - self.len) == 0):
                wdistance = 1
      

        for segment in self.segments:
            # NORTH
            if (self.x == segment.x) and (segment.y == (self.y + pxsize)):
                ndistance = 1
            # SOUTH
            if (self.x == segment.x) and (segment.y == (self.y - pxsize)):
                sdistance = 1
            # EAST
            if (self.y == segment.y) and (segment.x == (self.x + pxsize)):
                edistance = 1    
            # WEST
            if (self.y == segment.y) and (segment.x == (self.x - pxsize)):
                wdistance = 1


        if self.dir == pi/2 * 0: # East
            return([ndistance, edistance, sdistance])
        elif self.dir == pi/2 * 1: # North
            return([wdistance, ndistance, edistance])
        elif self.dir == pi/2 * 2: # West
            return([sdistance, wdistance, ndistance])
        elif self.dir == pi/2 * 3: # South
            return([edistance, sdistance, wdistance])
        else:
            return([None,None,None])


    def angle_point(self, point):
        """
            Angle to "food" relative to snake direction.
        """

        theta = arctan2(self.y - point.y, point.x - self.x) + self.dir

        # Normalize [-1, +1]
        if (theta > pi):
            theta -= 2*pi

        theta /= pi
  
        return(theta)


    def snake_vision(self, walls, point, width, height, pxsize):
        """
            Based on current position and direction of snake (head), calculate input array for neural network.
            Simplest setup:
                Four input neurons of distance to closest wall/snake segment directly 
                1) in front of snake, 
                   2) to the left,
                3) to the right, and
                4) angle to "food" relative to snake direction
                
        """
        #distances = self.nearst_wall(walls, width, height)
        distances = self.simple_nearest_wall(walls, pxsize)
        distances.append(self.angle_point(point))
        return([distances])


    def show(self):
        for segment in self.segments:
            segment.show()
        

