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
    # graph=RRTGraph(start,goal,dimensions,obsdim,obsnum)

    obstacles=graph.make_obs()

    # map.draw_map(obstacles)

    print("here")
    map.draw_map(obstacles)

    while(True):
        x,y = graph.sample_environment()
        n=graph.number_of_nodes()
        graph.add_node(n,x,y)
        if(graph.is_free()):
            pygame.draw.circle(map.map, map.red, (graph.x[n], graph.y[n]), map.node_rad, map.node_thickness)
        pygame.display.update()



if __name__ == '__main__':
    main()
