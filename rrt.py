import pygame
from rrtbasepy2 import RRTGraph, RRTMap
import numpy as np

class rrt_star():
    def __init__(self):
        self.iteration=0
        self.dimensions = (600,1000)
        self.start = (50,50)
        self.goal = (800, 510)
        self.obsdim=30
        self.obsnum=50
        self.valid_radius=100
        self.costs=self.create_costs()
        self.nodes=[]  
        self.links=[]

        pygame.init()
        self.graph=RRTGraph(self.start,self.goal,self.dimensions,self.obsdim,self.obsnum) #Graph
        self.map=RRTMap(self.start,self.goal,self.dimensions,self.obsdim,self.obsnum)

        self.obstacles=self.graph.make_obs()
        
    def execute(self):
        self.map.draw_map(self.obstacles)
        for i in range(0,3):
            node=self.graph.expand() 
            if node is not None:
                self.nodes.append(node)   
        node_near=self.graph.nearest(node)
        self.costs.insert(node[2], self.graph.distance(node, node_near))
        node_neighbours = self.graph.find_neighbours(node, self.valid_radius)
        print(f'node: {node}')
        print(f'valid nodes: {node_neighbours}')

        link=self.graph.chain(node, node_near)
        if link is not None:
            self.links.append(link)

        print(self.links)
        print(self.nodes)

        # for node_adjacent in node_neighbours:
        #     if self.costs

        # while (not graph.path_to_goal()): #for itr in range 
        #     # Xnew
        #     node = graph.pick_node(iteration)
        #     node_near = graph.nearest(node)
        #     print(f'node_near: {node_near}')

        #     # find neighbours


    def create_costs(self):
        costs=[]
        for i in range(0,2000):
            costs.append(2000)
        return costs






        #     iteration += 1


        #map.draw_path(graph.get_path_coords())
        pygame.display.update()
        pygame.event.clear()
        pygame.event.wait(0)

        # place 3 nodes, 1 inside the radius and 1 outside, see if function works as intended        
    


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
