# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 18:40:17 2014

@author: svyatoslav
"""

def next_num(i):
    if i == vertex_count - 1:
        return 0, True
    else:
        return i + 1, False

def prev_num(i):
    if i == 0:
        return vertex_count - 1
    else:
        return i - 1
        
def det(vertex1, vertex2, point):
    begin_vertex = vertex1
    a_1 = vertex2[0] - vertex1[0]
    b_1 = vertex2[1] - vertex1[1]
    if b_1 < 0:
        a_1 = -a_1
        b_1 = -b_1
        begin_vertex = vertex2
    a_2 = point[0] - begin_vertex[0]
    b_2 = point[1] - begin_vertex[1]
    return a_1 * b_2 - a_2 * b_1

# read stdin

vertex_count = 0
point_count = 0
vertex_list = []
point_list = []
vertex_count = int(raw_input())
for i in range(vertex_count):
    pair = raw_input()
    coords_str = pair.strip("()").split(",")
    coords = [int(c) for c in coords_str]
    vertex_list.append(coords)
point_count = int(raw_input())
for i in range(point_count):
    pair = raw_input()
    coords_str = pair.strip("()").split(",")
    coords = [int(c) for c in coords_str]
    point_list.append(coords)

# check points

# the ray is directed horizontally to the left

for point in point_list:
    checked = False
    x = point[0]
    y = point[1]

    # check whether the point coincides with some vertex
    for vertex in vertex_list:
        if vertex[0] == x and vertex[1] == y:
            print "yes"
            checked = True
            break
    if checked == True:
        continue

    # check whether the point lies on a side of the polygon
    for i in range(vertex_count):
        j, final_vertex_passed = next_num(i)
        vertex1 = vertex_list[i]
        vertex2 = vertex_list[j]
        min_x = min(vertex1[0], vertex2[0])
        max_x = max(vertex1[0], vertex2[0])
        if det(vertex1, vertex2, point) == 0 and x >= min_x and x <= max_x:
            print "yes"
            checked = True
            break
    if checked == True:
        continue
    
    # count intersections
    count = 0 # intersections counter
    final_vertex_passed = False
    counter = 0 # it is added to i to pass sides that were already considered inside the loop
    for i in range(vertex_count):
        if final_vertex_passed:
            break
        i += counter
        counter = 0
        j, final_vertex_passed = next_num(i)    
        vertex1 = vertex_list[i]
        vertex2 = vertex_list[j]
        min_y = min(vertex1[1], vertex2[1])
        max_y = max(vertex1[1], vertex2[1])
        det_value = det(vertex1, vertex2, point)
        if y >= min_y and y <= max_y and det_value <= 0:
            # there may be an intersection
            horizontal = False
            if det_value == 0 and y == vertex1[1]: 
                # the point lays on the horizontal line, connecting vertices 1, 2
                horizontal = True
                k = prev_num(i)
                vertex0 = vertex_list[k]
                begin_below = False
                # calc the true value of begin_below
                if vertex0[1] < y:
                    begin_below = True
                elif vertex0[1] == y and k == vertex_count - 1:
                    # we should consider horizontal sides behind the first vertex
                    horizontal1 = True
                    while horizontal1:
                        m = k
                        q = prev_num(m)
                        if vertex_list[q][1] < y:
                            begin_below = True
                            horizontal1 = False
                        elif vertex_list[q][1] > y:
                            begin_below = False
                            horizontal1 = False
                # if vertex0[1] == y but k != vertex_count - 1, then begin_below 
                # was defined previously
                # if vertex0[1] > y, then begin_below remains False
                while horizontal:
                    i = j
                    j, final_vertex_passed = next_num(j)
                    counter += 1
                    vertex1 = vertex_list[i]
                    vertex2 = vertex_list[j]
                    if det(vertex1, vertex2, point) != 0 or y != vertex1[1]:
                        horizontal = False
                        end_below = False
                        if vertex2[1] < y:
                            end_below = True
                        counter -= 1
                        continue
                    next_j, final_vertex_passed = next_num(j)
                    vertex3 = vertex_list[next_j]
                    end_below = False
                    if vertex3[1] < y:
                        end_below = True
                # check whether the ray intersects a series of horizontal sides
                if (begin_below and not end_below) or (not begin_below and end_below):
                    count += 1
                    continue
            else:
                if y > min_y and y < max_y:
                    count += 1
                    continue
                if y == min_y:
                    value = min_y
                else:
                    value = max_y
                if value == vertex1[1]:
                    vertex_num = i
                else:
                    vertex_num = j
                k = prev_num(vertex_num)
                vertex_prev = vertex_list[k]
                m, final_vertex_passed = next_num(vertex_num)
                vertex_next = vertex_list[m]
                if (vertex_prev[1] < y and vertex_next[1] > y) or (vertex_prev[1] > y and vertex_next[1] < y):
                    count += 1
                    counter += 1
                    
    # is the point inside or outside?
    if count % 2 == 0:
        print "no"
    else:
        print "yes"