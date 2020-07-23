library(openxlsx)


"READ IN DATA"
dataGenPop = readxl::read_xlsx("Z:\\CBP_CentralAmerica\\Gravity\\CBP_StatesCentroidPopulation.xlsx")
Validation_Matrix = readxl::read_xlsx("C:\\Users\\amarti32\\Desktop\\CBP_GenPop_ValidationData.xlsx")



"COMPUTE THE DISTANCE MATRIX"
x = dataGenPop$POINT_X
y = dataGenPop$POINT_Y

Points = cbind(x,y)

D = dist(Points, method = "euclidean", diag = TRUE, upper = TRUE)

DistMat = as.matrix(D)



"PREPARE INTERACTION MATRIX PARAMETERS"
IntMatrix = DistMat

Origin = dataGenPop$PopulationBirth
Destination = dataGenPop$PopulationResidence


"PREPARE THE CONSTANT VALUES"
LAMBDA = seq(0,2, length.out = 50)
ALPHA = seq(0,2, length.out = 50)
BETA = seq(0,2, length.out = 50)
K = seq(0,2, length.out = 50)



"COMPUTE INTERACTION MATRIX AND SAVE RESULTS TO LIST"
COUNT = 1
LAMBDA_LIST = c()
ALPHA_LIST = c()
BETA_LIST = c()
K_LIST = c()
CELLCOUNT_LIST = c()


while (COUNT <= 200){
  LAMBDA_VAL = LAMBDA[runif(1,1,50)]
  ALPHA_VAL = ALPHA[runif(1,1,50)]
  BETA_VAL = BETA[runif(1,1,50)]
  K_VAL = K[runif(1,1,50)]
  CELL_COUNT = 0
  
  for (j in 1:length(x)) {
    for (i in 1:length(x)) {
      if (DistMat[i,j] == 0) {
        IntMatrix[i,j] = (K_VAL*(Destination[i]^LAMBDA_VAL)* (Destination[j]^ALPHA_VAL)) / (DistMat[i,j] ^ 0)
      }
      else {
        IntMatrix[i,j] = (K_VAL*(Destination[i]^LAMBDA_VAL)* (Destination[j]^ALPHA_VAL)) / (DistMat[i,j] ^ BETA_VAL)
      }
    }
  }
  
  "ONCE INT MATRIX IS COMPLETE, CHECK EACH CELL TO SEE IF THE SUBTRACTION BETWEEN THE INT MATRIX AND VALIDATION MATRIX"
  "FALLS WITHIN A SPECIFIED TOLERANCE, IF YES INCREASE CELL COUNT, APPEND RESULST TO LIST, INCREASE WHILE COUNT"
  Subtract_Matrix = Validation_Matrix - IntMatrix
  for (i in 1:length(Subtract_Matrix)){
    for (j in 1:length(Subtract_Matrix)){
      if (abs(Subtract_Matrix[i,j]) <= 500){
        CELL_COUNT = CELL_COUNT + 1
      }
    }
  }
  
  LAMBDA_LIST = c(LAMBDA_LIST, LAMBDA_VAL)
  ALPHA_LIST = c(ALPHA_LIST, ALPHA_VAL)
  BETA_LIST = c(BETA_LIST, BETA_VAL)
  K_LIST = c(K_LIST, K_VAL)
  CELLCOUNT_LIST = c(CELLCOUNT_LIST, CELL_COUNT)
 
  COUNT = COUNT + 1
  
}


OPTIMAL_CELLCOUNT_INDEX = which(CELLCOUNT_LIST==max(CELLCOUNT_LIST))

OPT_LAMBDA = LAMBDA_LIST[OPTIMAL_CELLCOUNT_INDEX]
OPT_ALPHA = ALPHA_LIST[OPTIMAL_CELLCOUNT_INDEX]
OPT_BETA = BETA_LIST[OPTIMAL_CELLCOUNT_INDEX]
OPT_K = K_LIST[OPTIMAL_CELLCOUNT_INDEX]


OPT_INTMATRIX = DistMat


for (j in 1:length(x)) {
  for (i in 1:length(x)) {
    if (DistMat[i,j] == 0) {
      OPT_INTMATRIX[i,j] = (OPT_K*(Destination[i]^OPT_LAMBDA)* (Destination[j]^OPT_ALPHA)) / (DistMat[i,j] ^ 0)
    }
    else {
      OPT_INTMATRIX[i,j] = (OPT_K*(Destination[i]^OPT_LAMBDA)* (Destination[j]^OPT_ALPHA)) / (DistMat[i,j] ^ OPT_BETA)
    }
  }
}






