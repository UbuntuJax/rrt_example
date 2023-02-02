import pygame
from rrtbasepy import RRTGraph, RRTMap

def main():
    iteration=0
    dimensions = (600,1000)
    start = (50,50)
    goal = (800, 50)
    obsdim=30
    obsnum=100

    pygame.init()
    graph=RRTGraph(start,goal,dimensions,obsdim,obsnum)
    map=RRTMap(start,goal,dimensions,obsdim,obsnum)

    obstacles=graph.make_obs()
    map.draw_map(obstacles)


    while (not graph.path_to_goal()):
        if iteration % 10 == 0:
            x,y,parent=graph.bias(goal)
            pygame.draw.circle(map.map, map.grey,(x[-1],y[-1]),map.node_rad+2,0)
            pygame.draw.line(map.map,map.blue,(x[-1],y[-1]),(x[parent[-1]],y[parent[-1]]),\
                map.edge_thickness)

        else:
            x,y,parent=graph.expand()
            pygame.draw.circle(map.map, map.grey, (x[-1], y[-1]), map.node_rad+2,0)
            pygame.draw.line(map.map,map.blue,(x[-1],y[-1]),(x[parent[-1]],y[parent[-1]]),\
                map.edge_thickness)

        if iteration%5==0:
            pygame.display.update()
        iteration+=1
    
    map.draw_path(graph.get_path_coords())
    print(f'x: {graph.x}')
    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)



if __name__ == '__main__':
    # try:
    #     main()
    # except IndexError:
    #     print
    main()
