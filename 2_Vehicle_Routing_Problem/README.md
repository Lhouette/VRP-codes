# FORMULATION

***Sets:***  
$V$ : sets of customer nodes  
$K$ : sets of vhicles
  
***Parameters:***  
$c_{ij}$ : distance of traveling from node i to j  
$n$ : number of customer nodes  
  
***Variables:***  
$x^k_{ij}$ : 1 if vehicle k travels from node i to j, 0 otherwise  
$y^k_{i}$ : variables to remove sub-tour
  
  
## Objective function
 
$$min(Z) =\sum_{k\in K}\sum_{i\in V}\sum_{j\in V}c_{ij}x^k_{ij} $$

## subject-to

$\sum_{j\in V\setminus\left\\{0\right\\}} x^k_{0j}= 1,\\;\forall k\in K$  
$\sum_{i\in V\setminus\left\\{0\right\\}} x^k_{i0}= 1,\\;\forall k\in K$  
$\sum_{k\in K}\sum_{j\in V\setminus\left\\{i\right\\}} x^k_{ij}= 1,\\;\forall i\in V\setminus\left\\{0\right\\}$  
$\sum_{k\in K}\sum_{i\in V\setminus\left\\{j\right\\}} x^k_{ij}= 1,\\;\forall j\in V\setminus\left\\{0\right\\}$  
$\sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ij} = \sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ji},\\;\forall k\in K,\\;\forall i\in V\setminus\left\\{0\right\\}$  
$y^k_{i}-(n+1)x_{ij}\geq y^k_{j}-n,\\;\forall k\in K,\\;\forall i\in V\setminus\left\\{0\right\\},\\;\forall j\in V\setminus\left\\{0\right\\},\\;i\neq j$  
$x^k_{ij}\in \left\\{0, 1\right\\},\\;\forall i, j\in V$  
