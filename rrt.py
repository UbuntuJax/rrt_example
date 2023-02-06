import pygame
from rrtbasepy import RRTGraph, RRTMap

def main():
    iteration=0
    dimensions = (600,1000)
    start = (50,50)
    goal = (800, 510)
    obsdim=30
    obsnum=50
    valid_radius=100

    pygame.init()
    graph=RRTGraph(start,goal,dimensions,obsdim,obsnum) #Graph
    map=RRTMap(start,goal,dimensions,obsdim,obsnum)

    obstacles=graph.make_obs()
    map.draw_map(obstacles)


    # while (not graph.path_to_goal()): #for itr in range
    #     # Xnew
    #     if iteration % 5 ==0:
    #         print("bias")
    #         x,y,parent=graph.bias(goal)

    #     else:
    #         print("expand")
    #         x,y,parent=graph.expand()

    #     pygame.draw.circle(map.map, map.grey, (x[-1], y[-1]), map.node_rad+2,0)
    #     pygame.draw.line(map.map,map.blue,(x[-1],y[-1]),(x[parent[-1]],y[parent[-1]]),\
    #         map.edge_thickness)

    #     if iteration%5==0:
    #         pygame.display.update()
    #     iteration+=1

    #     # find neighbours
    
    # map.draw_path(graph.get_path_coords())
    # pygame.display.update()
    # pygame.event.clear()
    # pygame.event.wait(0)

    # place 3 nodes, 1 inside the radius and 1 outside, see if function works as intended
    graph.add_node(graph.number_of_nodes(), 50,52)
    graph.add_node(graph.number_of_nodes(), 500,500)
    graph.add_node(graph.number_of_nodes(), 51,50)
    graph.add_node(graph.number_of_nodes(), 510,500)
    print(graph.nearest(graph.number_of_nodes()-1))
    print(f'x: {graph.x[1]}, y: {graph.y[1]}')


if __name__ == '__main__':
    main()

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
