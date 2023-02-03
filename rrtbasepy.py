# contains classes and methods necessary to run rrt

import random
import math
import pygame

class RRTMap:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        """Initialise vars"""
        self.start=start
        self.goal=goal
        self.map_dimensions=map_dimensions
        self.maph,self.mapw=self.map_dimensions

        # colors
        self.grey = (70,70,70)
        self.blue = (0,0,255)
        self.green = (0,255,0)
        self.red = (255,0,0)
        self.white = (255,255,255)

        # window settings
        self.map_window_name='RRT path planning'
        pygame.display.set_caption(self.map_window_name)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.fill(self.white)
        self.node_rad=2
        self.node_thickness=0
        self.edge_thickness=1
        self.obsdim=obsdim
        self.obs_number=obsnum

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

class RRTGraph:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        """Initialise vars"""
        (x,y)=start
        self.start=start
        self.goal=goal
        self.goal_flag=False
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
        self.obs_pos=[] # list of tuples: [(xmin, xmax, ymin, ymax), (...), ...]
        self.obs_dim=obsdim
        self.obs_num=obsnum

        # path
        self.goal_state=None
        self.path=[]

    def make_obs(self):
        """Make a straight line of obstacles, then create extrusions"""
        obs=[]
        obs_pos=[]

        # straight line of obstacles
        for i in range(0, self.obs_num):
            rectangle=None
            upper=(i*25,200)
            rectangle=pygame.Rect(upper,(self.obs_dim, self.obs_dim))
            if rectangle.collidepoint(self.start) or rectangle.collidepoint(self.goal):
                i+=1
                continue
            obs.append(rectangle)
            pos=(upper[0], upper[0]+self.obs_dim, upper[1], upper[1]+self.obs_dim)
            obs_pos.append(pos)

        # extrusions
        for i in range(0, self.obs_num):
            y_pos = random.uniform(200,100)
            y_len = 200-y_pos
            upper = (i*50, y_pos)
            rectangle=pygame.Rect(upper,(self.obs_dim, y_len))
            if rectangle.collidepoint(self.start) or rectangle.collidepoint(self.goal):
                i+=1
                continue
            obs.append(rectangle)
            pos=(upper[0], upper[0]+self.obs_dim, upper[1], upper[1]+self.obs_dim)
            obs_pos.append(pos)


        # returning list
        self.obstacles=obs.copy()
        self.obs_pos=obs_pos.copy()
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

    def nearest(self, n):
        dmin=self.distance(0,n)
        n_near=0
        for i in range(0,n):
            if self.distance(i,n)<dmin:
                dmin=self.distance(i,n)
                n_near=i
        return n_near

    def nearest_y(self, n):
        # needs testing
        """Check x_pos of obs is valid, then check y dist from node to obstacle"""
        # get obstacle positions
        node_x=self.x[n]
        node_y=self.y[n]
        valid_nodes=[]
        y_pos=1000

        # find valid x nodes
        for i in self.obs_pos:
            if node_x <= i[1] and node_x >= i[0]:
                valid_nodes.append(i)

        # find closest y obstacle
        for i in valid_nodes:
            if i[3] < y_pos:
                y_pos = i[3]

        return y_pos # returns the pixel value


    def node_generation(self):
        n = self.number_of_nodes()
        print(f'n1: {n}')
        y = 50 # placeholder y_pos for generating nodes
        circle_locations=[]
        num_nodes=160
        space=1000/num_nodes
        
        for i in range(0,num_nodes):
            x = i * space + self.obs_dim/2
            # x = 0
            self.add_node(n, x, y)
            n = self.number_of_nodes()
            print(f'n2: {n}')
    
            # sample the closest obstacle in the y
            y_close = self.nearest_y(n-1)
            print(f'node: {x,y,n}')
            print(f'y_close: {y_close}')

            # save circle locations for main() to draw
            circle_locations.append((x, y_close-50))
        return circle_locations


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

    def step(self, n_near, n_rand, dmax=35):
        d=self.distance(n_near, n_rand)
        if d>dmax:
            u=dmax/d
            (x_near,y_near)=(self.x[n_near],self.y[n_near])
            (x_rand,y_rand)=(self.x[n_rand], self.y[n_rand])
            (px,py)=(x_rand-x_near,y_rand-y_near)
            theta=math.atan2(py,px)
            (x,y)=(int(x_near+dmax*math.cos(theta)),\
                int(y_near+dmax*math.sin(theta)))
            self.remove_node(n_rand)
            if abs(x-self.goal[0])<dmax and abs(y-self.goal[1])<dmax:
                self.add_node(n_rand, self.goal[0], self.goal[1])
                self.goal_state=n_rand
                self.goal_flag=True

            else:
                self.add_node(n_rand,x,y)

    def path_to_goal(self):
        if self.goal_flag:
            self.path=[]
            self.path.append(self.goal_state)
            new_pos = self.parent[self.goal_state]
            while new_pos!=0:
                self.path.append(new_pos)
                new_pos=self.parent[new_pos]
            self.path.append(0)
        return self.goal_flag

    def get_path_coords(self):
        path_coords=[]
        for node in self.path:
            x,y=(self.x[node], self.y[node])
            path_coords.append((x,y))
        return path_coords

    def bias(self, n_goal):
        n = self.number_of_nodes()
        self.add_node(n,n_goal[0], n_goal[1])
        n_near=self.nearest(n)
        self.step(n_near,n)
        self.connect(n_near, n)
        return self.x, self.y, self.parent

    def expand(self):
        n=self.number_of_nodes()
        x,y=self.sample_environment()
        self.add_node(n,x,y)
        if self.is_free():
            n_near=self.nearest(n)
            self.step(n_near,n)
            self.connect(n_near,n)
        return self.x, self.y, self.parent

    def cost(self):
        pass