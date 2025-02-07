import numpy as np
import Data_Pipeline_Test as dpt
import sys
import os
import cv2
import glob
from PIL import Image #Need to import this to do image editing


#### Visualizer
def pad(array, shape):
    print(array.shape, shape)
    board = np.zeros(shape)
    # area = [0: array.shape[0],0: array.shape[1],0: array.shape[2]]
    board[0: array.shape[0],0: array.shape[1],0: array.shape[2]] = array
    return board

char_2_tile_path = {
         "X": '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/X.png',
        "S" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/S.png',
        "-" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/-.png',
        "?" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/Q.png',
        "Q" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/Q.png',
        "E" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/E.png',
        "<" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/PTL.png',
        ">" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/PTR.png',
        "[" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/[.png',
        "]" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/].png',
        "o" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/o.png',
        "B" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/0.png',
        "b" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/0.png',
        "#" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/#.png',
        "D" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/D.png',
        "H" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/H.png',
        "M" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/M.png',
        "T" : '/Users/mohammadrezahami/Documents/University/PCG/Project/Code/sprites/T.png',
        }

def get_tiles():
  char_2_tile = {}
  for char, path in char_2_tile_path.items():
    img = cv2.imread(path) 
    
    char_2_tile[char] = pad(img, shape=(16,16,3))

  return char_2_tile

char_2_tile = get_tiles()


def visualize_ga(chunk):
  img = np.zeros(shape=(14 * 16, 16 * 16, 3))

  row_idx = 0
  col_idx = 0

  for row in chunk:
    for char in row:
      img[row_idx:row_idx+16, col_idx:col_idx+16, :] = char_2_tile[char]
      col_idx += 16
    row_idx += 16
    col_idx = 0

  return img


def visualize(individual):
    
    #Load the set of all sprites
    sprites = {}
    for filename in glob.glob(os.path.join(os.getcwd(), "sprites", "*.png")):
        im = Image.open(filename)
        splits = filename.split("/")
        name = splits[-1][:-4]
        sprites[name] = im.convert('RGBA')

    #This gives the mapping between the tile values and the associated sprite
    visualization = {}
    visualization["X"] = "X1"
    visualization["S"] = "S"
    visualization["-"] = "-"
    visualization["?"] = "Q"
    visualization["Q"] = "Q"
    visualization["E"] = "E"
    visualization["<"] = "PTL"
    visualization[">"] = "PTR"
    visualization["["] = "pipe"
    visualization["]"] = "pipe_r"
    visualization["o"] = "o"
    #visulization["B"] = ""
    #visulization["b"] = 
    visualization["T"] = "T"
    visualization["M"] = "M"
    visualization["D"] = "D"
    visualization["#"] = "X"
    visualization["H"] = "H"

    # This reads in the level
    # level = {}
    # with open(os.path.join(os.getcwd(), "Generated Levels", "output.txt")) as fp:
    #     y = 0
    #     for line in fp:
    #         level[y] = line
    #         y+=1

    #Multiply by 18 here as each of the sprites is 14*16
    image = Image.new("RGB", (14*len(individual[0]), 16*len(individual)), color=(223, 245, 244)) #This creates an initially blank image for the level
    pixels = image.load() #This loads the level image's pixels so we can edit them

    maxY = len(individual)
    maxX = len(individual[0])

    for y in range(0, maxY):
        for x in range(0, maxX):
            imageToUse = None
            if individual[y][x] in visualization.keys():
                imageToUse = sprites[visualization[individual[y][x]]]
                #print(imageToUse)
            #elif individual[y][x]=="X":
                #Rules we've added to ensure the correct sprite is used
                #if y==maxY-2:
                   # imageToUse = sprites["groundTop"]
                # elif y==maxY-1:
                #     #Check if we have a solid tile above this and change which sprite we use if so
                #     if individual[y-1][x]=="X":
                #         imageToUse = sprites["groundBottom"]
                #     else:
                #         imageToUse = sprites["groundTop"]
                # else:
                #     imageToUse = sprites["stair"]

            if not imageToUse == None:
                #If we have a sprite (imageToUse) copy its pixels over
                pixelsToUse = imageToUse.load()
                for x2 in range(0, 13):
                    for y2 in range(0, 15):
                        if pixelsToUse[x2,y2][3]>0:
                            pixels[x*14+x2,y*16+y2] = pixelsToUse[x2,y2][0:-1]
    return image


def mutation(individual, mutation_rate):
    if np.random.random()<mutation_rate:
        
        ###attempt1
        ## change one cell to soomething random between 1 and 16
        row = np.random.randint(0,len(individual))
        column = np.random.randint(0,len(individual[0]))
        smb_elements = ['S','?','Q','E','<','>','[',']','o','B','b']
        kl_elements = ['T','M','D','H']
        elements = smb_elements + kl_elements
        individual[row][column] = elements[np.random.randint(0,15)]
        return individual

        ###attempt2
        ## swap 2 cells of the individual
        # row_1 = np.random.randint(0,len(individual))
        # column_1 = np.random.randint(0,len(individual[0]))

        # row_2 = np.random.randint(0,len(individual))
        # column_2 = np.random.randint(0,len(individual[0]))

        # while not (row_1==row_2 and column_1==column_2):
        #     row_2 = np.random.randint(0,len(individual))
        #     column_2 = np.random.randint(0,len(individual[0]))
        # tmp = individual[row_1][column_1]
        # individual[row_1][column_1] = individual[row_2][column_2]
        # individual[row_2][column_2] = tmp
        # return individual
    else:
        return individual

def crossover(individual_1, individual_2, crossover_rate):
    child_1 = np.array([[]]).reshape(0,16)
    child_2 = np.array([[]]).reshape(0,16)
    if np.random.random()<crossover_rate:
        
        # if np.random.randint(0,2):
        if 0:
            ##crossover by row
            
            rand_row_cut = np.random.randint(0, 13)
            child_1 = np.concatenate((child_1,individual_1[:rand_row_cut+1]))
            #child_1 = individual_1[:rand_row_cut+1]
            child_1 = np.concatenate((child_1,individual_2[rand_row_cut+1:]))
            #child_1 += individual_2[rand_row_cut+1:]


            child_2 = np.concatenate((child_2,individual_1[rand_row_cut+1:]))
            #child_2 = individual_1[rand_row_cut+1:]
            child_2 = np.concatenate((child_2,individual_2[:rand_row_cut+1]))
            #child_2 += individual_2[:rand_row_cut+1]

            return child_1, child_2

        else:
            ##crossover by column
            rand_cul_cut = np.random.randint(0, 14)
            for row in range(len(individual_1)):
                temp1 = np.array([[]]).reshape(0,16)
                temp1 = np.concatenate((individual_1[row][:rand_cul_cut+1],individual_2[row][rand_cul_cut+1:]))
                #child_1=individual_1[row][:rand_cul_cut+1]
                temp1 = np.array([temp1])
                child_1 = np.concatenate((child_1,temp1))
                #child_1[row] += individual_2[row][rand_cul_cut+1:]

                temp2 = np.array([[]]).reshape(0,16)
                temp2 = np.concatenate((individual_1[row][rand_cul_cut+1:],individual_2[row][:rand_cul_cut+1]))
                #child_2.append(individual_1[row][rand_cul_cut+1:])
                #child_2[row] += individual_2[row][:rand_cul_cut+1]
                temp2 = np.array([temp2])
                child_2 = np.concatenate((child_2,temp2))

            return child_1, child_2
    else:
        return child_1, child_2

def evolution(population, population_limit,passable_point,passable_smb_sum,passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum):
    newpopulation = []
    fitness_population = []
    for individual in population:
        fitness_population.append((fitness(individual, passable_point,passable_smb_sum,passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum), individual))

    # np.sort(fitness_population,axis=0)

    fitness_population.sort(key=lambda tup: tup[0], reverse=True)
    for i in range(population_limit//5*4):
        newpopulation.append(fitness_population[i][1])

    ## also append some random trash
    inthelist = []
    for i in range(population_limit//5):
        rand_individual = np.random.randint(len(population)//5*4,len(population))


        while rand_individual in inthelist:
            rand_individual = np.random.randint(len(population)//5*4,len(population))
        
        newpopulation.append(fitness_population[rand_individual][1])
        inthelist.append(rand_individual)
    
    return newpopulation

def fitness(individual, passable_point,passable_smb_sum,passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum):
    distribution = {}
    smb_elements = ['X','S','-','?','Q','E','<','>','[',']','o','B','b']
    kl_elements = ['T','M','D','#','H','-']
    elements = smb_elements + kl_elements
    distribution = dpt.distribution_extractor(individual, elements, distribution)


    passable = ['o','-','M','T']
    solid = ['X','S','?','Q', '#','H']
    passable_sum = 0
    solid_sum = 0

    for key in distribution:
        if key in passable:
            passable_sum += distribution[key]
        elif key in solid:
            solid_sum += distribution[key]

    #print("solid",solid_sum)

    #for passable
    fitness_passable = 0
    if passable_smb_sum <= passable_kid_sum:
        if passable_sum >= passable_smb_sum and passable_sum <= passable_point:
            fitness_passable = ((passable_point - passable_sum) / (passable_smb_sum - passable_point)) + 1

        elif passable_sum <= passable_kid_sum and passable_sum >= passable_point:
            fitness_passable = ((passable_point - passable_sum) / (passable_kid_sum - passable_point)) + 1
        else:
            fitness_passable = 0
    else:
        if passable_sum >= passable_kid_sum and passable_sum <= passable_point:
            fitness_passable = ((passable_point - passable_sum) / (passable_kid_sum - passable_point)) + 1

        elif passable_sum <= passable_smb_sum and passable_sum >= passable_point:
            fitness_passable = ((passable_point - passable_sum) / (passable_smb_sum - passable_point)) + 1
        else:
            fitness_passable = 0

    
    # print("passable_sum:",passable_sum)
    # print("passable_smb:",passable_smb_sum)
    # print("passable_kid:",passable_kid_sum)
    # print("passable_point:",passable_point)
    # print("passable_fitness:",fitness_passable)

    #for solid
    fitness_solid = 0
    if solid_smb_sum <= solid_kid_sum:
        if solid_sum >= solid_smb_sum and solid_sum <= solid_point:
            fitness_solid = ((solid_point - solid_sum) / (solid_smb_sum - solid_point)) + 1

        elif solid_sum <= solid_kid_sum and solid_sum >= solid_point:
            fitness_solid = ((solid_point - solid_sum) / (solid_kid_sum - solid_point)) + 1
        else:
            fitness_solid = 0
    else:
        if solid_sum >= solid_kid_sum and solid_sum <= solid_point:
            fitness_solid = ((solid_point - solid_sum) / (solid_kid_sum - solid_point)) + 1

        elif solid_sum <= solid_smb_sum and solid_sum >= solid_point:
            fitness_solid = ((solid_point - solid_sum) / (solid_smb_sum - solid_point)) + 1
        else:
            fitness_solid = 0
    
    fitness= (fitness_passable + fitness_solid)/2

    return fitness

def generation(population:list, crossover_rate, mutation_rate, population_limit, passable_point,passable_smb_sum,passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum):
    ##select parents
    for _ in range(len(population)//3):
        parent_1 = np.random.randint(0,len(population))
        parent_2 = np.random.randint(0,len(population))
        while parent_1 == parent_2:
            parent_2 = np.random.randint(0,len(population))
        child_1, child_2 = crossover(population[parent_1], population[parent_2], crossover_rate)
        ##do crossover
        if child_1.size != 0 and child_2.size != 0:
            population.append(child_1)
            population.append(child_2)

    ##do mutation
    for individual in population:
        individual = mutation(individual, mutation_rate)
    
    ##do evolution
    population = evolution(population, population_limit, passable_point,passable_smb_sum,passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum)

    return population


def main():
    num_generation = 500
    population = []
    crossover_rate = 0.8
    mutation_rate = 0.05
    population_limit = 250
    blending_point = 0.33
    mario_address = 'mario-3-3.txt'
    kidicarus_address = 'kidicarus_1.txt'
    passable_point,passable_smb_sum,passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum = dpt.points_extractor(mario_address, kidicarus_address,blending_point)

    dataset_smb, dataset_kid = dpt.dataset_creator(mario_address,kidicarus_address)

    population = dataset_kid + dataset_smb

    for epoch in range(num_generation):
        print("-----",epoch,"-----")
        population = generation(population, crossover_rate, mutation_rate, population_limit, passable_point, passable_smb_sum, passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum)
    
    fitness_population = []
    for individual in population:
        fitness_population.append((fitness(individual, passable_point,passable_smb_sum,passable_kid_sum, solid_point, solid_smb_sum, solid_kid_sum), individual))

    fitness_population.sort(key=lambda tup: tup[0], reverse=True)

    i = 0
    for individual in fitness_population[:50]:
        #print(individual[1],individual[0])
        #print("------------------------------------------")
        #print("------------------------------------------")
        image = visualize_ga(individual[1])
        cv2.imwrite("output"+str(i)+'.png',image)
        # image.save("./outputs/output"+str(i)+".jpeg","JPEG")
        i += 1
        print("output ",str(i),": ",individual[0])

if __name__ == main():
    main()
    
