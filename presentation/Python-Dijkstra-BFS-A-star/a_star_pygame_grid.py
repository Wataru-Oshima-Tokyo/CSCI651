
import pygame as pg
from heapq import *
from random import random
from collections import deque
import time
import sys
import math
import numpy as np
from memory_profiler import profile
import matplotlib.pyplot as plt

def get_circle(x, y):
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


def get_neighbours(x, y):
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1] #8 ways to go
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.circle(sc, pg.Color('red'), *get_circle(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dynamic_heuristic(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def make_grid(random_,t,dstar):
    dstar = False
    global grid
    grid = [[]]
    if random_:
        for row in range(rows):
            grid.append([])
            for col in range(cols):
                if random() < 0.2 and (row!=0 and col !=7):
                    grid[row].append(100)
                else:
                    grid[row].append(0)
    else:
        for row in range(rows):
            grid.append([])
            for col in range(cols):
                #first rectangle
                if (abs(row-t) >= rows//3 and abs(row-t) <=rows//2) and (col >= cols//3 and col <=cols//2):
                    grid[row].append(100)
                #second rectangle
                elif (row >= rows//2 and row <=rows-rows//10) and (abs(col-t) >= cols//2 and abs(col-t) <=cols-cols//10):
                    grid[row].append(100)
                #third triangle
                elif math.sqrt(pow((row -t),2)+ pow((col-t),2))<8:
                    grid[row].append(100) 
                #first circle
                elif math.sqrt(pow((row*2 -t),2)+ pow((col-t),2))<10:
                    grid[row].append(100) 
                #second circle
                elif math.sqrt(pow((row -t),2)+ pow(((cols-col)-t),2))<10:
                        grid[row].append(100) 
                else:
                    grid[row].append(0)


def detect_obstacle(v):
    global grid
    detected = False
    if grid[v[1]][v[0]] >= 100:
        print("object detected")
        detected = True
    return  detected

def dijkstra_dstar(start_, goal_, graph):
    global grid,start_time,start
    queue = [] #this is the open List
    heappush(queue, (0, goal_))  # added the start_ point to the open List
    cost_visited = {goal_: 0} #make a closed cost list with the start_ point
    visited = {goal_: None} #make a closed node list with the start_ point
    while queue:
        cur_cost, cur_node = heappop(queue) #get the node with the minimum cost from the open List
        if cur_node == start_: ## if the point is the goal_ then break it
            break

        neighbours = graph[cur_node] #get the neibours of the current node
        for neighbour in neighbours: #for each neighbor, the below operation will be applied
            neigh_cost, neigh_node = neighbour # get the cost and coordinate of the neigbor
            new_cost = cost_visited[cur_node] + neigh_cost #calculate the new cost with the cost of current node + the neighbour's cost

            #if the neighbor has not been visited yet and the new cost is less than the cost to go to the goal_ from the neighbour
            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]: 
                # calculate g(n) + h(n) which is the cost of node itself + the linear distance from this neighbour to the goal_
                priority = new_cost + heuristic(neigh_node, goal_) 
                heappush(queue, (priority, neigh_node)) # add the node and new cost to the openList 
                cost_visited[neigh_node] = new_cost #update the cost of the node in the closed cost list
                visited[neigh_node] = cur_node #update the node to visited node in the closed visited list
    return visited






def bfs(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0} 
    visited = {start: None}
    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited



def dijkstra_astar(start_, goal_, graph):
    global grid
    queue = [] #this is the open List
    heappush(queue, (0, start_))  # added the start_ point to the open List
    cost_visited = {start_: 0} #make a closed cost list with the start_ point
    visited = {start_: None} #make a closed node list with the start_ point
    while queue:
        cur_cost, cur_node = heappop(queue) #get the node with the minimum cost from the open List
        if cur_node == goal_: ## if the point is the goal_ then break it
            break

        neighbours = graph[cur_node] #get the neibours of the current node
        for neighbour in neighbours: #for each neighbor, the below operation will be applied
            neigh_cost, neigh_node = neighbour # get the cost and coordinate of the neigbor
            new_cost = cost_visited[cur_node] + neigh_cost #calculate the new cost with the cost of current node + the neighbour's cost

            #if the neighbor has not been visited yet and the new cost is less than the cost to go to the goal_ from the neighbour
            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]: 
                # calculate g(n) + h(n) which is the cost of node itself + the linear distance from this neighbour to the goal_
                priority = new_cost + heuristic(neigh_node, goal_) 
                heappush(queue, (priority, neigh_node)) # add the node and new cost to the openList 
                cost_visited[neigh_node] = new_cost #update the cost of the node in the closed cost list
                visited[neigh_node] = cur_node #update the node to visited node in the closed visited list
    return visited
# @profile
def main(cols, rows, dynamic, astar, dstar, visualize):
    global average_time


    # adjacency dict
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)

    start = (0, 7)
    initial_start = start
    next_node = None
    next_next_node = None
    goal = (cols-1, rows-1)
    queue = []
    heappush(queue, (0, start))
    visited = {start: None}
    start_time = time.time()
    total_time = 0.0
    t_=0
    temp = (0,7)
    initial_flag = True
    visited_path =[]
    path_counter = 0
    # while True:
    
    attempts = 0
    while(1):
        # fill screen
        if t_>rows*time_stamp:
            t_=1
        else:
            t_+=1
        if start == initial_start and not initial_flag:
            # start = (0, 7)
            attempts +=1 
            print("The time to reach the goal  is ", total_time)
            average_time.append(total_time)
            total_time = 0.0
            initial_flag = True
            path_counter =0
            if attempts == 20:
                break
            

        if visualize:
            sc.fill(pg.Color('black'))
            #draw the cost cells
            [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
            for x, col in enumerate(row) if grid[y][x] >=100] for y, row in enumerate(grid)]
            [[pg.draw.rect(sc, pg.Color('purple'), get_rect(x, y), border_radius=TILE // 5)
            for x, col in enumerate(row) if grid[y][x] <100 and grid[y][x] >=50] for y, row in enumerate(grid)]
            [[pg.draw.rect(sc, pg.Color('green'), get_rect(x, y), border_radius=TILE // 5)
            for x, col in enumerate(row) if grid[y][x] <50 and grid[y][x] >=30] for y, row in enumerate(grid)]
            [[pg.draw.rect(sc, pg.Color('white'), get_rect(x, y), border_radius=TILE // 5)
            for x, col in enumerate(row) if grid[y][x] <30 and grid[y][x] >=10] for y, row in enumerate(grid)]
            # bfs, get path to mouse click
            pg.draw.circle(sc, pg.Color('red'), *get_circle(goal[0],goal[1]))
        if dynamic:
            make_grid(random_=False,t=t_//time_stamp, dstar=False)
            # adjacency dict
            graph = {}
            for y, row in enumerate(grid):
                for x, col in enumerate(row):
                    graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)
        mouse_pos = None
        if visualize:
            mouse_pos = get_click_mouse_pos() 
        if mouse_pos:
            goal = mouse_pos
        start_time = time.time()
        detcted = False
        if astar:
            if dstar and not initial_flag:
                # if detecct_obstacle(goal):
                detcted = detect_obstacle(start)
                if detcted:
                    visited = dijkstra_astar(start, goal, graph)
                    path_counter =0        
                else:
                    try:
                        start = visited_path[path_counter+3]    
                        path_counter+=1  
                    except:
                        start = initial_start
                    pass
            else:
                visited = dijkstra_astar(start, goal, graph)
        else:
            visited = bfs(start, goal, graph)
        # goal = mouse_pos
        end_time = time.time()
        total_time += (end_time-start_time)
        # print("The time to find a path is ", (end_time-start_time))
        
        # draw path
        path_head, path_segment = goal, goal
        temp = initial_start
        

        visited_path =[]
        while path_segment and path_segment in visited:
            if visualize:
                pg.draw.rect(sc, pg.Color('black'), get_rect(path_segment[0], path_segment[1]))
                pg.draw.circle(sc, pg.Color('blue'), *get_circle(*path_segment))
            path_segment = visited[path_segment] 
            visited_path.append(path_segment)
            if path_segment != None:
                if path_segment == start:
                    pass
                else:   
                    temp = path_segment
        
        visited_path.reverse()
        if dstar and not initial_flag:
            if detcted:
               start = temp 
        else:
            start = temp
        initial_flag = False

        
        print("current node: ",start)
        # next_node = visited[start]
        # print("next node: ",visited_path[2])
        # print(visited)
        if visualize:
            pg.draw.circle(sc, pg.Color('green'), *get_circle(*start))
            pg.draw.circle(sc, pg.Color('magenta'), *get_circle(*goal))
        # pygame necessary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    if len(sys.argv) == 8:
        cols, rows, dynamic, astar, dstar, visualize, debug = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]), int(sys.argv[7])
    else:
        cols, rows, dynamic, astar, dstar,visualize,debug = 100,100,1,1,1,0,1
    average_time_total =[]
    
    TILE = 5
    time_stamp = 3




    #debug:



    if debug:
        if visualize:
            pg.init()
            sc = pg.display.set_mode([cols * TILE, rows * TILE])
        clock = pg.time.Clock()
        grid =[[]]
        make_grid(random_=False,t=20, dstar=dstar)
        average_time = []
        main(cols, rows, dynamic, astar, dstar, visualize)
        map_type =""
        algorithm =""
        if dynamic:
            map_type = "dynamic"
        else:
            map_type = "static"

        if dstar:
            algorithm = "D star algorithm"
        elif astar:
            algorithm = "A star algorithm"
        else:
            algorithm = "BFS algorithm"
        print("The average Time to reach the goal in %s %d x %d map by %s is %lf" %(map_type, cols, rows, algorithm, np.mean(average_time)))
    else:
        plot_number = 221
        plt.figure() 
        _counter = 0
        _cols = [20,50,100,150,200]
        cells = [i*i for i in _cols]
        colors = ["red", "green", "blue", "orange"]
        
        dstar = False
        dynamic = False
        for p in range(2):
            for j in range(2):
                # plt.subplot(plot_number)
                for i in range(5):
                    cols = rows = _cols[i]
                    if visualize:
                        pg.init()
                        sc = pg.display.set_mode([cols * TILE, rows * TILE])
                    clock = pg.time.Clock()
                    grid =[[]]
                    make_grid(random_=False,t=20, dstar=dstar)
                    average_time = []
                    main(cols, rows, dynamic, astar, dstar, visualize)
                    average_time_total.append(np.mean(average_time))
                map_type =""
                algorithm =""
                if dynamic:
                    map_type = "Dynamic"
                else:
                    map_type = "Static"

                if dstar:
                    algorithm = "D star algorithm"
                elif astar:
                    algorithm = "A star algorithm"
                else:
                    algorithm = "BFS algorithm"
                label =  "%s map by %s" %(map_type,algorithm)
                plt.scatter(cells, average_time_total, color=colors[_counter],label=label,alpha=0.3, edgecolors='none')
                plot_number+=1
                dstar = True
                average_time_total =[]
                _counter +=1
            dstar = False
            dynamic = True   
        # 
        # plt.errorbar(ps, harmonic_centrality_total, yerr=std_error, fmt="o", color="red")
        # plt.yscale("log")
        plt.xlabel('Number of cells ')
        plt.ylabel('Time')
        plt.title('A star vs D star (Time)')
        plt.legend()
        plt.show()

