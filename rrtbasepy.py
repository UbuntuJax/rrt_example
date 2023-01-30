# contains classes and methods necessary to run rrt

import random
import math
import pygame

class RRTMap:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        self.start=start
        self.goal=goal
        self.map_dimensions=map_dimensions
        self.maph,self.mapw=self.map_dimensions

        # window settings
        self.map_window_name='RRT path planning'
        pygame.display.set_caption(self.map_window_name)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.fill((255,255,255))
        self.node_rad=2
        self.node_thickness=0
        self.edge_thickness=1

        self.obstacles=[]
        self.obsdim=obsdim
        self.obs_number=obsnum

        # colors
        self.grey = (70,70,70)
        self.blue = (0,0,255)
        self.green = (0,255,0)
        self.red = (255,0,0)
        self.white = (255,255,255)

    def draw_map(self, obstacles):
        pygame.draw.circle(self.map, self.green, self.start, self.node_rad+5,0)
        pygame.draw.circle(self.map, self.red, self.goal, self.node_rad+20,1)
        self.draw_obs(obstacles)

    def draw_path(self):
        pass

    def draw_obs(self, obstacles):
        obstacles_list = obstacles.copy()
        while (len(obstacles_list) > 0):
            obstacle=obstacles_list.pop(0)
            pygame.draw.rect(self.map, self.grey, obstacle)

class RRTGraph:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        (x,y)=start
        self.start=start
        self.goal=goal
        self.goalFlag=False
        self.maph,self.mapw = map_dimensions
        self.x=[]
        self.y=[]
        self.parent=[]

        # initialise the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        # the obstacles
        self.obstacles=[]
        self.obs_dim=obsdim
        self.obsNum=obsnum

        # path
        self.goal_state=None
        self.path=[]

    def make_random_rect(self):
        upper_corner_x=int(random.uniform(0,self.mapw-self.obs_dim))
        upper_corner_y=int(random.uniform(0,self.maph-self.obs_dim))

        return (upper_corner_x,upper_corner_y)

    def make_obs(self):
        obs=[]

        for i in range(0, self.obsNum):
            rectangle=None
            start_goal_col = True
            while start_goal_col:
                upper = self.make_random_rect()
                rectangle=pygame.Rect(upper,(self.obs_dim, self.obs_dim))
                if rectangle.collidepoint(self.start) or rectangle.collidepoint(self.goal):
                    start_goal_col=True
                else:
                    start_goal_col=False
            obs.append(rectangle)
        self.obstacles=obs.copy()
        return obs

    def add_node(self,n,x,y):
        self.x.insert(n,x)
        self.y.append(y)

    def remove_node(self,n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self,parent,child):
        self.parent.insert(child,parent)

    def remove_edge(self,n):
        self.parent.pop(n)

    def number_of_nodes(self):
        return len(self.x)

    def distance(self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        px=(float(x1)-float(x2))**2
        py=(float(y1)-float(y2))**2
        return (px+py)**(0.5)

    def sample_environment(self):
        x=int(random.uniform(0,self.mapw))
        y=int(random.uniform(0,self.maph))
        return x,y

    def nearest(self):
        pass

    def is_free(self):
        n=self.number_of_nodes()-1
        (x,y)=(self.x[n],self.y[n])
        obs=self.obstacles.copy()
        while len(obs)>0:
            rectangle=obs.pop(0)
            if rectangle.collidepoint(x,y):
                self.remove_node(n)
                return False
            return True

    def cross_obstacle(self,x1,x2,y1,y2):
        obs=self.obstacles.copy()
        while(len(obs)>0):
            rectangle=obs.pop(0)
            for i in range(0,101):
                u=i/100
                x=x1*u+x2*(1-u)
                y=y1*u+y2*(1-u)
                if rectangle.collidepoint(x,y):
                    return True
        return False

    def connect(self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        if self.cross_obstacle(x1,x2,y1,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2)
            return True

    def step(self):
        pass

    def path_to_goal(self):
        pass

    def get_path_coords(self):
        pass

    def bias(self):
        pass

    def expand(self):
        pass

    def cost(self):
        pass