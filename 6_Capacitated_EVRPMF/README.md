# FORMULATION 

***Sets:***  
$V$ : sets of all nodes  
$\left\\{0\right\\}$ : depot node  
$V_n$ : sets of customer nodes  
$V_e$ : sets of charging station nodes  
$V_c$ : sets of fuel station nodes  
  
$K$ : sets of all vehicles  
$K_c$ : sets of (CV)conventional vehicles  
$K_e$ : sets of (EV)electric vehicles  
  
***Parameters:***  
$c_{ij}$ : distance of traveling from node i to j  
$C_c$ : storage capacity of CV  
$C_e$ : storage capacity of EV  
$Q_c$ : fuel capacity of CV  
$Q_e$ : battery capacity of EV  
$r_c$ : ratio of fuel consumption and distance of CV  
$r_e$ : ratio of battery consumption and distance of EV  
  
***Variables:***  
$x^k_{ij}$ : 1 if vehicle k travels from node i to j, 0 otherwise  
$y^k_i$ : variables to remove sub-tour  
$u1^k_{i}$ : fuel or battery level when vehicle starts from node i  
$u2^k_{i}$ : fuel or battery level when vehicle arrives node i  
%s^k_i% : storage load when vehicle starts from node i
  
  
## Objective function 
for the shortest total distance  
$$min(Z) =\sum_{k\in K}\sum_{i\in V}\sum_{j\in V}c_{ij}x^k_{ij} $$

## subject-to

$\sum_{j\in V\setminus\left\\{0\right\\}} x^k_{0j}\leq 1,\\;\forall k\in K$  
$\sum_{i\in V\setminus\left\\{0\right\\}} x^k_{i0}\leq 1,\\;\forall k\in K$  
$\sum_{k\in K}\sum_{j\in V\setminus\left\\{i\right\\}} x^k_{ij}= 1,\\;\forall i\in V_n$  
$\sum_{k\in K}\sum_{i\in V\setminus\left\\{j\right\\}} x^k_{ij}= 1,\\;\forall j\in V_n$  
$\sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ij} = \sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ji},\\;\forall k\in K,\\;\forall i\in V$  
$u1^k_0=Q_c,\\;\forall k\in K_c$  
$u1^k_0=Q_e,\\;\forall k\in K_e$  
$u1^k_i=Q_c,\\;\forall k\in K_c,\\;\forall i\in V_c$  
$u1^k_i=Q_e,\\;\forall k\in K_e,\\;\forall i\in V_e$  
$x^k_{ij}, x^k_{ji}=0,\\;\forall k\in K_c,\\;\forall i\in V_e,\\;\forall j\in V$  
$x^k_{ij}, x^k_{ji}=0,\\;\forall k\in K_e,\\;\forall i\in V_c,\\;\forall j\in V$  
$u1^k_i, u2^k_i\geq 0,\\;\forall k\in K,\\;\forall i\in V$  
$u1^k_i, u2^k_i\leq Q_c,\\;\forall k\in K_c,\\;\forall i\in V$  
$u1^k_i, u2^k_i\leq Q_e,\\;\forall k\in K_e,\\;\forall i\in V$  
$u1^k_i-r_cc_{ij}x^k_{ij}+Q_c(1-x^k_{ij})\geq u2^k_i,\\;\forall k\in K_c,\\;\forall i, j\in V\setminus\left\\{0\right\\}, i\neq j$  
$u1^k_i-r_ec_{ij}x^k_{ij}+Q_e(1-x^k_{ij})\geq u2^k_i,\\;\forall k\in K_e,\\;\forall i, j\in V\setminus\left\\{0\right\\}, i\neq j$  
$y^k_{i}-(n+1)x_{ij}\geq y^k_{j}-n,\\;\forall k\in K,\\;\forall i\in V\setminus\left\\{0\right\\},\\;\forall j\in V\setminus\left\\{0\right\\},\\;i\neq j$  
$u1^k_i=u2^k_i,\\;\forall k\in K,\\;\forall i\in V$  
$x^k_{ij}\in \left\\{0, 1\right\\},\\;\forall i, j\in V$  

# Result Example Image

<img src="https://github.com/Lhouette/VRP-codes/blob/main/6_Capacitated_EVRPMF/result-CEVRPMF.png?raw=true"/>
