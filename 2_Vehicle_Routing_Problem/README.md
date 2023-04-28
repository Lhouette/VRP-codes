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

1. $\sum_{j\in V\setminus\left\\{0\right\\}} x_{0j}= K$  
2. $\sum_{i\in V\setminus\left\\{0\right\\}} x_{i0}= K$  
3. $\sum_{j\in V\setminus\left\\{i\right\\}} x_{ij}= 1,\\;\forall i\in V\setminus\left\\{0\right\\}$  
4 .$\sum_{i\in V\setminus\left\\{j\right\\}} x_{ij}= 1,\\;\forall j\in V\setminus\left\\{0\right\\}$  
5. $y_{i}-(n+1)x_{ij}\geq y_{j}-n,\\;\forall i\in V\setminus\left\\{0\right\\},\\;\forall j\in V\setminus\left\\{0\right\\},\\;i\neq j$  
6. $x_{ij}\in \left\\{0, 1\right\\},\\;\forall i, j\in V$  
