import pygame
from rrtbasepy import RRTGraph, RRTMap

def main():
    dimensions = (600,1000)
    start = (50,50)
    goal = (510, 510)
    obsdim=30
    obsnum=50

    pygame.init()
    graph=RRTGraph(start,goal,dimensions,obsdim,obsnum)
    map=RRTMap(start,goal,dimensions,obsdim,obsnum)

    obstacles=graph.make_obs()

    map.draw_map(obstacles)

    while(True):
        x,y = graph.sample_environment()
        n=graph.number_of_nodes()
        graph.add_node(n,x,y)
        graph.add_edge(n-1,n)
        x1,y1=graph.x[n],graph.y[n]
        x2,y2=graph.x[n-1],graph.y[n-1]
        if(graph.is_free()):
            pygame.draw.circle(map.map, map.red, (graph.x[n], graph.y[n]), map.node_rad, map.node_thickness)
            if not graph.cross_obstacle(x1,x2,y1,y2):
                pygame.draw.line(map.map, map.blue,(x1,y1),(x2,y2),map.edge_thickness)

        pygame.display.update()



if __name__ == '__main__':
    main()
