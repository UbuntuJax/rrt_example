import pygame
from rrtbasepy2 import RRTGraph, RRTMap
import numpy as np
X_VAL=0
Y_VAL=1
INDEX=2

class rrt_star():
    def __init__(self):
        self.iteration=0
        self.dimensions = (600,1000)
        self.start = (50,50)
        self.goal = (800, 510)
        self.obsdim=30
        self.obsnum=50
        self.valid_radius=100
        self.costs={}
        # self.parents={}
        # self.nodes=[]
        self.parents={32:59}
        self.nodes=[(246, 21, 32), ((11, 22, 59))]  
        self.links=[]
        self.optimal_links={}
        print(self.optimal_links)
        self.add_start()

        pygame.init()
        self.graph=RRTGraph(self.start,self.goal,self.dimensions,self.obsdim,self.obsnum) #Graph
        self.map=RRTMap(self.start,self.goal,self.dimensions,self.obsdim,self.obsnum)

        self.obstacles=self.graph.make_obs()
        
    def execute(self):
        for _ in range(0,3000):
            self.map.draw_map(self.obstacles)
            node=self.graph.expand()
            self.costs[node[INDEX]]=20000 #set each node to have extreme cost so that any path will be better 
            if node is None:
                continue   
            else:
                self.nodes.append(node)
            node_near=self.graph.nearest(node, self.valid_radius)
            if node_near is None:
                continue

            self.costs[node[INDEX]]=self.graph.distance(node, node_near)
            node_neighbours = self.graph.find_neighbours(node, self.valid_radius)

            link=self.graph.chain(node, node_near)
            if link is not None:
                self.links.append(link)

            for node_adjacent in node_neighbours:
                if self.costs[node[2]] + self.graph.distance(node, node_adjacent) < self.costs[node_adjacent[INDEX]]:
                    self.costs[node_adjacent[INDEX]]=self.costs[node[INDEX]] + self.graph.distance(node, node_adjacent)
                    self.parents[node_adjacent[INDEX]]=node[INDEX]
                    self.optimal_links[node[INDEX]]=node_adjacent[INDEX]

        print(f'Optimal links: {self.optimal_links}')
        self.draw_map()

        pygame.display.update()
        pygame.event.clear()
        pygame.event.wait(0)    
    
    def add_start(self):
        self.costs[0]=0
        self.nodes.append((self.start[0], self.start[1], 0))

    def draw_map(self):
        for i in self.optimal_links:
            node, parent = self.get_node_info(i)
            pygame.draw.circle(self.map.map, self.map.grey, (node[X_VAL], node[Y_VAL]), self.map.node_rad+2,0)
            if parent is not None:
                pygame.draw.line(self.map.map,self.map.blue,(node[X_VAL], node[Y_VAL]),\
                    (parent[X_VAL], parent[Y_VAL]), self.map.edge_thickness)

    def get_node_info(self, node_index):
        # returns xy co-ords for the node and the parent node
        node=(self.nodes[node_index][X_VAL], self.nodes[node_index][Y_VAL])
        try:
            parent_index=self.parents[node_index]
            parent=(self.nodes[parent_index][X_VAL], self.nodes[parent_index][Y_VAL])
        except KeyError:
            parent = None 
        return node, parent


if __name__ == '__main__':
    search=rrt_star()
    search.execute()

# rrt* psuedocode
"""
Rad = r
G(V,E) //Graph containing edges and vertices
For itr in range(0…n)
    Xnew = RandomPosition()
    If Obstacle(Xnew) == True, try again
    Xnearest = Nearest(G(V,E),Xnew)
    Cost(Xnew) = Distance(Xnew,Xnearest)
    Xbest,Xneighbors = findNeighbors(G(V,E),Xnew,Rad)
    Link = Chain(Xnew,Xbest)
    For x’ in Xneighbors
        If Cost(Xnew) + Distance(Xnew,x’) < Cost(x’)
            Cost(x’) = Cost(Xnew)+Distance(Xnew,x’)
            Parent(x’) = Xnew
            G += {Xnew,x’}
    G += Link 
Return G
"""
