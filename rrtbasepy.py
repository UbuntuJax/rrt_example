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
        self.map_window_name='RRT* path planning'
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

    def draw_path(self, path):
        for node in path:
            pygame.draw.circle(self.map, self.red, node, self.node_rad+3,0)

    def draw_obs(self, obstacles):
        obstacles_list = obstacles.copy()
        while (len(obstacles_list) > 0):
            obstacle=obstacles_list.pop(0)
            pygame.draw.rect(self.map, self.grey, obstacle)

    def redraw(self, x_y_parent_list):
        """
        Wipes the map and redraws it (important when you're adding and removing nodes)

        Attributes:
            x_y_parent_list: list of the x and y positions of each node as well as the parent index
            of the previous node
        """

class RRTGraph:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        (x,y)=start
        self.start=start
        self.goal=goal
        self.goal_flag=False
        self.maph,self.mapw = map_dimensions
        self.node_list=[(x,y,0),]
        self.n=1

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

    def pick_node(self,iteration):
        #parent is unused
        if iteration % 5 ==0:
            print("bias")
            x,y,n=self.bias(self.goal)

        else:
            print("expand")
            x,y,n=self.expand()

        node = (x,y,n)
        return node


    def bias(self):
        pass

    def expand(self):
        x,y=self.sample_environment()
        while(not self.is_free(x,y)):
            x,y=self.sample_environment()
        self.add_node(x,y)
        return self.node_list[-1]

    def sample_environment(self):
        x=int(random.uniform(0,self.mapw))
        y=int(random.uniform(0,self.maph))
        return x,y

    def is_free(self,x,y):
        #checks if a node is inside an obstacle
        obs=self.obstacles.copy()
        while len(obs)>0:
            rectangle=obs.pop(0)
            if rectangle.collidepoint(x,y):
                return False
            return True

    def add_node(self,x,y):
        #adds a node and increments the node index value
        self.node_list.append((x,y,self.n))
        self.n+=1

    def nearest(self, node):
        node_near=None
        start_node=self.node_list[0]
        dmin=self.distance(start_node, node)
        node_near=start_node
        for i in range(1,self.number_of_nodes()):
            distance=self.distance(self.node_list[i], node)
            if distance<dmin and self.node_list[i] != node:
                dmin=distance
                node_near=self.node_list[i]

        return node_near

    def distance(self, node1, node2):
        x1=node1[0]
        x2=node2[0]
        y1=node1[1]
        y2=node2[1]
        px=(float(x1)-float(x2))**2
        py=(float(y1)-float(y2))**2
        return (px+py)**(0.5)

    def number_of_nodes(self):
        return len(self.node_list)

    def find_neighbours(self, node, valid_radius=100):
        """
        Returns all nodes within a set radius of the parent

        Attributes:
            Radius is the area within which the function will consider when declaring valid nodes
            (relative to the parent node)

        Returns:
            valid nodes are the neighbours surrounding the current node
        """
        valid_nodes=[]

        for i in range(0,self.number_of_nodes()):
            if self.distance(node, self.node_list[i]) < valid_radius and self.node_list[i] != node:
                valid_nodes.append(self.node_list[i])
            else:
                #print(f'rejected node {self.node_list[i]} or rejected self')
                pass

        return valid_nodes

    def chain(self, node1, node2):
        if not self.cross_obstacle(node1[0], node2[0], node1[1], node2[1]):
            return (node2[2], node1[2])
        else:
            return None

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
