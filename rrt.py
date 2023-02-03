import pygame
from rrtbasepy import RRTGraph, RRTMap

def main():
    iteration=0
    dimensions = (600,1000)
    start = (50,50)
    goal = (800, 50)
    obsdim=30
    obsnum=100
    parent=None

    pygame.init()
    graph=RRTGraph(start,goal,dimensions,obsdim,obsnum)
    map=RRTMap(start,goal,dimensions,obsdim,obsnum)

    obstacles=graph.make_obs()
    map.draw_map(obstacles)

    circle_locations=graph.node_generation()

    # draw circles at places identified by node_generation
    for x,y in circle_locations: 
        pygame.draw.circle(map.map, map.grey,(x,y),map.node_rad+2,0)
        if parent is not None:
            pygame.draw.line(map.map,map.blue,(x,y),(parent[0], parent[1]),\
                map.edge_thickness)
        parent=(x,y)
        
    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)



if __name__ == '__main__':
    # try:
    #     main()
    # except IndexError:
    #     print
    main()
