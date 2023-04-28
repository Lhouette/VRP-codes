# FORMULATION

***Sets:***  
$V$ : sets of customer nodes  
  
***Parameters:***  
$c_{ij}$ : distance of traveling from node i to j  
$n$ : number of customer nodes  
$K$ : number of Vehicles  
  
***Variables:***  
$x_{ij}$ : 1 if vehicle travels from node i to j, 0 otherwise  
$y_{ij}$ : variables to remove sub-tour


## Objective function
 
$$min(Z) =\sum_{i\in V}\sum_{j\in V}c_{ij}x_{ij} $$

## subject-to

$$
\sum_{j\in V\setminus\left\\{0\right\\}} x_{0j}= K
$$  
$$
\sum_{i\in V\setminus\left\\{0\right\\}} x_{i0}= K  
$$
