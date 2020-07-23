#Code written by Adam Martin, START, UNIVERSITY OF MARYLAND

import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
import random
import time


"""
PSEUDOCODE:

Read in state centroid xy and population data
Read in validation data containing the matrix of actual population flows

Set variable x to the x coordinate data
Set variable y to the y coordinate data
Create variable points as a pandas dataframe consisting of the xy variables
Compute the distance matrix

Create variable for interaction matrix, initially set as copy of distance matrix
Create variable for birth population data
Create variable for residence population data

Create variable to store the possible values for LAMBDA
Create variable to store the possible values for ALPHA
Create variable to store the possible values for BETA
Create variable to store the possible values for K


Initialize variable for COUNT, set to 0
Initialize variable for RESULTS_LIST, set to empty list object

While COUNT is less than or equal to a pre-determined number: (ex. 500000)
    Randomly index value from the possible LAMBDA values
    Randomly index value from the possible ALPHA values
    Randomly index value from the possible BETA values
    Randomly index value from the possible K values
    Initialize a CELL_COUNT variable with 0
    
    For j in  range of the length of X:
        For i in range of the length of X:
            if Distance Matrix value is 0:
                Interaction Matrix[i][j] equals K*(PopResidence[i]**LAMBDA)*(PopResidence[j]**ALPHA) / DistMatrix[i][j]**0
            else:
                Interaction Matrix[i][j] equals K*(PopResidence[i]**LAMBDA)*(PopResidence[j]**ALPHA) / DistMatrix[i][j]**BETA
    
    Create variable which holds the matrix resulting from the subtraction of the interaction matrix and the validation matrix
    
    For i in range of length of subtraction matrix:
        for j in range of length of subtraction matrix:
            if absolute value of subtraction matrix[i][j] is less than or equal to 1000:
                CELL_COUNT increased by 1
            
    Append a dictionary of the LAMBDA, ALPHA, BETA, K and the CELL_COUNT values to the RESULTS_LIST
    Increment the While loop count by 1

Create a new list to store all the CELL_COUNT values from the RESULTS_LIST
Use the index of the maximum value to select the optimal values dictionary from the RESULTS_LIST
Print the dictionary contents to the console 


Initialize variable to store the optimal LAMBDA value 
Initialize variable to store the optimal ALPHA value 
Initialize variable to store the optimal BETA value 
Initialize variable to store the optimal K value 
Initialize varaible to store Optimal Interaction Matrix by copying the distance matrix again

Recompute the Interaction matrix using the optimal values

"""
start_time = time.time()

"Read in data"
dataGenPop = pd.read_excel("Z:\\CBP_CentralAmerica\\Gravity\\CBP_StatesCentroidPopulation.xlsx")
Validation_Matrix = pd.read_excel("C:\\Users\\amarti32\\Desktop\\CBP_GenPop_ValidationData.xlsx", sheet_name = "Data_WeightedPrisonPop")



"Calculate the distance matrix"
X = dataGenPop["POINT_X"]
Y = dataGenPop["POINT_Y"]

points = pd.concat([X,Y], axis=1)

DistMatrix = pd.DataFrame(distance_matrix(points.values, points.values), index=points.index, columns = points.index)



"""
"Output the distance matrix to list form in csv format"


DistData = list()

for i in range(len(X)):
    for j in range(len(X)):
        DATA = ["Distance between city {} and {}".format(i+1,j+1), DistMatrix[i][j]]
        DistData.append(DATA)
        
        
DistanceDataFrame = pd.DataFrame(DistData, columns = ["Cities","Distance"])

DistanceDataFrame.to_csv("DistancesBetweenCities.csv", index = False)

"""



"Prepare and Compute the Interaction Matrix"
IntMatrix = DistMatrix.copy()
PopBirth = dataGenPop["PopulationBirth"]
PopResidence = dataGenPop["PopulationResidence"]


"prepare the constant values"
LAMBDA = np.linspace(.6,1.2,50)
ALPHA = np.linspace(.6,1.2,50)
BETA = np.linspace(0,.5,50)
K = np.linspace(0,.001,50)

print("Data loaded and Distance matrix computed\n")


"Compute the interaction matrix and save results to a dict-list"
COUNT = 0
RESULTS_LIST = list()

print("Beginning computation of interaction matrices...\n")

while COUNT <= 10:
    LAMBDA_VAL = LAMBDA[random.randint(0,49)]
    ALPHA_VAL = ALPHA[random.randint(0,49)]
    BETA_VAL = BETA[random.randint(0,49)]
    K_VAL = K[random.randint(0,49)]
    CELL_COUNT = 0
    
    for j in range(len(X)):
        for i in range(len(X)):
            "Need to account for diagonal values where there is no movement between points"
            if DistMatrix[i][j] == 0:
                IntMatrix[i][j] = K_VAL*((PopResidence[i])**LAMBDA_VAL)* ((PopResidence[j])**ALPHA_VAL) / ((DistMatrix[i][j])**0)
            else:
                IntMatrix[i][j] = K_VAL*((PopResidence[i])**LAMBDA_VAL)* ((PopResidence[j])**ALPHA_VAL) / ((DistMatrix[i][j])**BETA_VAL)
    
    "once the IntMatrix is complete, check each cell after subtracting the IntMatrix from the Validation Matrix, if the difference"
    "falls within a tolerance of 0, add to the count of cells within this tolerance, append to results list, increase while count by 1"
    Subtract_Matrix = Validation_Matrix-IntMatrix
    for i in range(len(Subtract_Matrix)):
        for j in range(len(Subtract_Matrix)):
            if abs(Subtract_Matrix[i][j]) <= 50:
                CELL_COUNT += 1
  
    RESULTS_LIST.append({"Lambda":LAMBDA_VAL, "Alpha":ALPHA_VAL, "Beta":BETA_VAL, "K":K_VAL, "Cell Count":CELL_COUNT})
    
    if COUNT == 50000 or COUNT == 100000 or COUNT == 150000 or COUNT == 200000:
        timeToReach = time.time() - start_time
        print("Reached simulation number:",COUNT)
        print("Time to reach: {:.2f} seconds".format(timeToReach))
        
    COUNT += 1




"Store all the matrix sum values in a new list, check for the index of the min value"
"return the optimal parameters based on the index of the maximum cell count parameter"
SubMat_Values =[x["Cell Count"] for x in RESULTS_LIST]
OPTIMAL_PARAMS = RESULTS_LIST[SubMat_Values.index(max(SubMat_Values))]   
OPT_LAMBDA = OPTIMAL_PARAMS["Lambda"]
OPT_ALPHA = OPTIMAL_PARAMS["Alpha"]
OPT_BETA = OPTIMAL_PARAMS["Beta"]
OPT_K = OPTIMAL_PARAMS["K"]

print("Interaction matrices computed successfully\n")
print("The optimized parameters are:")
print(" Lambda: {:.4f} \n Alpha: {:.4f} \n Beta: {:.4f} \n K: {:.4f}".format(OPT_LAMBDA, OPT_ALPHA, OPT_BETA, OPT_K))



"Compute the interaction matrix with the optimal parameters"

OPT_IntMatrix = DistMatrix.copy()
for j in range(len(X)):
    for i in range(len(X)):
        "Need to account for diagonal values where there is no movement between points"
        if DistMatrix[i][j] == 0:
            OPT_IntMatrix[i][j] = OPT_K*((PopResidence[i])**OPT_LAMBDA)* ((PopResidence[j])**OPT_ALPHA) / ((DistMatrix[i][j])**0)
        else:
            OPT_IntMatrix[i][j] = OPT_K*((PopResidence[i])**OPT_LAMBDA)* ((PopResidence[j])**OPT_ALPHA) / ((DistMatrix[i][j])**OPT_BETA)


print("\nInteraction matrix computed using optimized parameters")


elapsed_time = time.time() - start_time
print("Time elapsed: {:.2f} seconds".format(elapsed_time))



