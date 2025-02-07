import numpy as np

smb_elements = ['X','S','-','?','Q','E','<','>','[',']','o','B','b']

kl_elements = ['T','M','D','#','H','-']

smb_passable = ['o','-']

smb_solid = ['X','S','?','Q']

kid_passable = ['-','M','T']

kid_solid = ['#','H','D']

smb_dictionary = {}
kl_dictionary = {}


# def map_encoder(map_array,map_type):

#     if map_type == "smb":
#         map_array[map_array == 'X1'] = 0
#         map_array[map_array == 'S1'] = 1
#         map_array[map_array == '-1'] = 2
#         map_array[map_array == '?1'] = 3
#         map_array[map_array == 'Q1'] = 4
#         map_array[map_array == 'E1'] = 5
#         map_array[map_array == '<1'] = 6
#         map_array[map_array == '>1'] = 7
#         map_array[map_array == '[1'] = 8
#         map_array[map_array == ']1'] = 9
#         map_array[map_array == 'o1'] = 10
#         map_array[map_array == 'B1'] = 11
#         map_array[map_array == 'b1'] = 12

#     elif map_type == "kl":
#         map_array[map_array == 'T1'] =  13
#         map_array[map_array == 'M1'] =  14
#         map_array[map_array == 'D1'] =  15
#         map_array[map_array == '#1'] =  16
#         map_array[map_array == 'H1'] =  17
#         map_array[map_array == '-1'] =  18

#     return map_array


def texter(address2, address1):
    stacked_list=[]
    with open(address1) as f:
        for line in f :
            line_list=[]
            for element in line:
                if element != '\n':
                    # line_list.append(element+'1')
                    line_list.append(element)

            line_list2 = np.array(line_list)
            # line_list3 = map_encoder(line_list2,'smb')
            # stacked_list.append(line_list3)

            stacked_list.append(line_list2)

    stacked_array=np.array(stacked_list)
    # print(stacked_array)

    stacked_list_1=[]
    with open(address2) as f:
        for line in f :
            line_list=[]

            for element in line:
                if element != '\n':
                    # line_list.append(element+'1')
                    line_list.append(element)
            line_list2 = np.array(line_list)        
            # line_list3 = map_encoder(line_list2,'kl')
            # stacked_list_1.append(line_list3)

            stacked_list_1.append(line_list2)

    stacked_array_1=np.array(stacked_list_1)
    # print(stacked_array_1)

    return stacked_array, stacked_array_1


def distribution_extractor(map, elements, distributions:dict):
    total_elements = len(map) * len(map[0])
    for element in elements:
        cnt = 0
        if len(element)==2:
            element = element[0]
        if element not in distributions:
            for row in map:
                for entity in row:
                    if entity == element:
                        cnt += 1
            distributions[element] = float(cnt/total_elements)
    return distributions


def dfs_util(map, node_x, node_y, visited, element_size):
    visited[node_x][node_y] = True
    element_size[node_x][node_y] = True

    same_neighbours = []

    if node_x-1>=0 and map[node_x][node_y] == map[node_x-1][node_y]:
        same_neighbours.append((node_x-1, node_y))
    if node_x+1<len(visited) and map[node_x][node_y] == map[node_x+1][node_y]:
        same_neighbours.append((node_x+1, node_y))
    if node_y+1<len(visited[0]) and map[node_x][node_y] == map[node_x][node_y+1]:
        same_neighbours.append((node_x, node_y+1))
    if node_y-1>=0 and map[node_x][node_y] == map[node_x][node_y-1]:
        same_neighbours.append((node_x, node_y-1))
    
    for node in same_neighbours:
        if not visited[node[0]][node[1]]:
            dfs_util(map, node[0], node[1], visited, element_size)


def count_connected_objects(map):
    cnt = 0
    visited = [[False for _ in range(len(map[0]))] for _ in range(len(map))]
    element_size = [[False for _ in range(len(map[0]))] for _ in range(len(map))]
    elements_sizes = []
    for node_x in range(len(map)):
        for node_y in range(len(map[0])):
            if not visited[node_x][node_y]:
                dfs_util(map, node_x, node_y, visited, element_size)
                size = 0
                for row in element_size:
                    for element in row:
                        if element:
                            size +=1
                elements_sizes.append(size)
                element_size = [[False for _ in range(len(map[0]))] for _ in range(len(map))]
                cnt += 1
    
    return cnt, elements_sizes

# a = [[1,1,1,3,2,3,5,6,1,1,1],
#      [1,1,1,3,2,3,5,6,6,1,1],
#      [1,1,1,1,2,2,5,5,5,5,5]]

# print(count_connected_objects(a))

def dataset_creator(address_1, address_2):
    map1, map2 = texter(address_1, address_2)
    dataset_kid = []
    ## create segments of kidicarus 14*16
    for i in range(len(map1)-14):
        dataset_kid.append(map1[i:i+14])
    # print(len(dataset[0][0]))

    dataset_smb = []
    ## create segmets of smb
    for i in range(len(map2[0])-16):
        segment = []
        for row in map2:
            segment.append(list(row[i:i+16]))
        dataset_smb.append(segment)
    
    
    return dataset_smb, dataset_kid


def points_extractor(mario_addresses, kid_addresses, blending_point):
    total_distributions_smb = {}
    total_distributions_kid = {}

    dataset_smb, dataset_kid = dataset_creator(mario_addresses, kid_addresses)
    
    for map in dataset_smb:
        distributions_smb = {}
        distributions_smb = distribution_extractor(map,smb_elements,distributions_smb)

        for key in distributions_smb:

            if key not in total_distributions_smb:
                total_distributions_smb[key] = distributions_smb[key]
            else:
                total_distributions_smb[key] += distributions_smb[key]

    for key in total_distributions_smb:
        total_distributions_smb[key] /= len(dataset_smb)

    for map in dataset_kid:
        distributions_kid = {}
        distributions_kid = distribution_extractor(map,kl_elements,distributions_kid)

        for key in distributions_kid:
            if key not in total_distributions_kid:
                total_distributions_kid[key] = distributions_kid[key]
            else:
                total_distributions_kid[key] += distributions_kid[key]

    for key in total_distributions_kid:
        total_distributions_kid[key] /= len(dataset_kid)
    
    passable_smb_sum = 0
    solid_smb_sum = 0
    passable_kid_sum = 0
    solid_kid_sum = 0

    for key in total_distributions_smb:
        if key in smb_passable:
            passable_smb_sum += total_distributions_smb[key]
        elif key in smb_solid:
            solid_smb_sum += total_distributions_smb[key]

    for key in total_distributions_kid:
        if key in kid_passable:
            passable_kid_sum += total_distributions_kid[key]
        elif key in kid_solid:
            solid_kid_sum += total_distributions_kid[key]

    if passable_kid_sum < passable_smb_sum:
        blending_point = 1 - blending_point
    
    passable_point = min(passable_smb_sum, passable_kid_sum) + abs(passable_kid_sum - passable_smb_sum) * blending_point
    solid_point = min(solid_smb_sum, solid_kid_sum) + abs(solid_kid_sum - solid_smb_sum) * blending_point

    return passable_point,passable_smb_sum,passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum


        

        




