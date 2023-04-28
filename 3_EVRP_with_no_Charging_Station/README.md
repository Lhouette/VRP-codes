# FORMULATION

***Sets:***  
$V$ : sets of customer nodes  
$K$ : sets of vhicles
  
***Parameters:***  
$c_{ij}$ : distance of traveling from node i to j  
$Q$ : battery capacity of vehicle  
$r$ : ratio of fuel consumption and distance  
  
***Variables:***  
$x^k_{ij}$ : 1 if vehicle k travels from node i to j, 0 otherwise  
$u1^k_{i}$ : battery level when vehicle starts from node i
$u2^k_{i}$ : battery level when vehicle arrives node i
  
  
## Objective function 
for the shortest total distance  
$$min(Z) =\sum_{k\in K}\sum_{i\in V}\sum_{j\in V}c_{ij}x^k_{ij} $$

## subject-to

$\sum_{j\in V\setminus\left\\{0\right\\}} x^k_{0j}= 1,\\;\forall k\in K$  
$\sum_{i\in V\setminus\left\\{0\right\\}} x^k_{i0}= 1,\\;\forall k\in K$  
$\sum_{k\in K}\sum_{j\in V\setminus\left\\{i\right\\}} x^k_{ij}= 1,\\;\forall i\in V\setminus\left\\{0\right\\}$  
$\sum_{k\in K}\sum_{i\in V\setminus\left\\{j\right\\}} x^k_{ij}= 1,\\;\forall j\in V\setminus\left\\{0\right\\}$  
$\sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ij} = \sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ji},\\;\forall k\in K,\\;\forall i\in V\setminus\left\\{0\right\\}$  
$u1^k_0=Q,\\;\forall k\in K$  
$x^k_{ij}\in \left\\{0, 1\right\\},\\;\forall i, j\in V$  

# Result Example Image

<img src="https://github.com/Lhouette/VRP-codes/blob/main/3_EVRP_with_no_Charging_Station/result-EVRPnCS.png?raw=true"/>
