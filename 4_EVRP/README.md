# FORMULATION

***Sets:***  
$V$ : sets of all nodes  
$N$ : sets of customer nodes  
$M$ : sets of charging station nodes  
$K$ : sets of vehicles
  
***Parameters:***  
$c_{ij}$ : distance of traveling from node i to j  
$Q$ : battery capacity of vehicle  
$r$ : ratio of fuel consumption and distance  
  
***Variables:***  
$x^k_{ij}$ : 1 if vehicle k travels from node i to j, 0 otherwise  
$y^k_i$ : variables to remove sub-tour  
$u1^k_{i}$ : battery level when vehicle starts from node i  
$u2^k_{i}$ : battery level when vehicle arrives node i
  
  
## Objective function 
for the shortest total distance  
$$min(Z) =\sum_{k\in K}\sum_{i\in V}\sum_{j\in V}c_{ij}x^k_{ij} $$

## subject-to

$\sum_{j\in V\setminus\left\\{0\right\\}} x^k_{0j}= 1,\\;\forall k\in K$  
$\sum_{i\in V\setminus\left\\{0\right\\}} x^k_{i0}= 1,\\;\forall k\in K$  
$\sum_{k\in K}\sum_{j\in N\setminus\left\\{i\right\\}} x^k_{ij}= 1,\\;\forall i\in N$  
$\sum_{k\in K}\sum_{i\in N\setminus\left\\{j\right\\}} x^k_{ij}= 1,\\;\forall j\in N$  
$\sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ij} = \sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ji},\\;\forall k\in K,\\;\forall i\in V\setminus\left\\{0\right\\}$  
$u1^k_0=Q,\\;\forall k\in K$  
$u1^k_i=!,\\;\forall k\in K,\\;\forall i\in M$  
$u1^k_i, u2^k_i\geq 0,\\;\forall k\in K,\\;\forall i\in V$  
$u1^k_i, u2^k_i\leq Q,\\;\forall k\in K,\\;\forall i\in V$  
$u1^k_i-rc_{ij}x^k_{ij}+Q(1-x^k_{ij})\geq u2^k_i,\\;\forall k\in K,\\;\forall i, j\in V\setminus\left\\{0\right\\}, i\neq j$  
$y^k_{i}-(n+1)x_{ij}\geq y^k_{j}-n,\\;\forall k\in K,\\;\forall i\in V\setminus\left\\{0\right\\},\\;\forall j\in V\setminus\left\\{0\right\\},\\;i\neq j$  
$u1^k_i=u2^k_i,\\;\forall k\in K,\\;\forall i\in V$  
$x^k_{ij}\in \left\\{0, 1\right\\},\\;\forall i, j\in V$  

# Result Example Image

<img src="https://github.com/Lhouette/VRP-codes/blob/main/4_EVRP/result-EVRP.png?raw=true"/>
