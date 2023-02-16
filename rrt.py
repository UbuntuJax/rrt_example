import pygame
from rrtbasepy import RRTGraph, RRTMap
import numpy as np
X_VAL=0
Y_VAL=1
INDEX=2

class rrt_star():
    def __init__(self):
        self.iteration=0
        self.dimensions = (600,1000)
        self.start = (50,50)
        self.goal = (510, 510)
        self.obsdim=30
        self.obsnum=50

        pygame.init()
        self.graph=RRTGraph(self.start,self.goal,self.dimensions,self.obsdim,self.obsnum) #Graph
        self.map=RRTMap(self.start,self.goal,self.dimensions,self.obsdim,self.obsnum)

        self.obstacles=self.graph.make_obs()
        
    def execute(self):
        for _ in range(0,3): #3000
            self.map.draw_map(self.obstacles)
            node=self.graph.expand() #generate random node
            node_xy=(node[X_VAL], node[Y_VAL])
            print(f'node: {node}')

            node_near_id=self.graph.nearest(node_xy) #get closest node and return id
            if node_near_id is None:
                continue

            new_vertex=self.graph.new_vertex(node_xy, node_near_id)
            print(f'new_vertex: {new_vertex}')
            print(f'node_neighbours: {self.graph.node_neighbours}')


        #     # generate a vertex that is limited by stepsize

        #     self.costs[node[INDEX]]=self.graph.distance(node, node_near)
        #     node_neighbours = self.graph.find_neighbours(node, self.valid_radius)

        #     link=self.graph.chain(node, node_near)
        #     if link is not None:
        #         self.links.append(link)

        #     for node_adjacent in node_neighbours:
        #         if self.costs[node[2]] + self.graph.distance(node, node_adjacent) < self.costs[node_adjacent[INDEX]]:
        #             self.costs[node_adjacent[INDEX]]=self.costs[node[INDEX]] + self.graph.distance(node, node_adjacent)
        #             self.parents[node_adjacent[INDEX]]=node[INDEX]
        #             self.optimal_links[node[INDEX]]=node_adjacent[INDEX]

        # print(f'Optimal links: {self.optimal_links}')
        # self.draw_map()

        # pygame.display.update()
        # pygame.event.clear()
        # while(1):
        #     pygame.event.wait(0)   

    def draw_map(self):
        for i in self.graph.optimal_links:
            node, parent = self.get_node_info(i)
            pygame.draw.circle(self.map.map, self.map.grey, (node[X_VAL], node[Y_VAL]), self.map.node_rad+2,0)
            if parent is not None:
                pygame.draw.line(self.map.map,self.map.blue,(node[X_VAL], node[Y_VAL]),\
                    (parent[X_VAL], parent[Y_VAL]), self.map.edge_thickness)

    def get_node_info(self, node_index):
        # returns xy co-ords for the node and the parent node
        node=(self.graph.nodes[node_index][X_VAL], self.graph.nodes[node_index][Y_VAL])
        try:
            parent_index=self.graph.parents[node_index]
            parent=(self.graph.nodes[parent_index][X_VAL], self.graph.nodes[parent_index][Y_VAL])
        except KeyError:
            parent = None 
        return node, parent


if __name__ == '__main__':
    search=rrt_star()
    search.execute()
