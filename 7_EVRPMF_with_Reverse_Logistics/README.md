# ASSUMPTION

- There is electirc vehicle(EV) and conventional vehicle(CV) 
- Each vehicle must be at depot when each route ends
- One of the vehicle must arrive to customer nodes once.
- Total number of new products can't exceed total capacity of all vehicle
- Total number of old products can't exceed total capacity of all vehicle

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
$d_i$ : The number of products desired by the consumer node i  
$p_i$ : The number of goods that need to be collected from consumer node i  
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
$s^k_i$ : load of new product when vehicle k starts from node i
$r^k_i$ : load of product collected by vehicle k starts from node i
  
## Objective function 
for the shortest total distance  
$$min(Z) =\sum_{k\in K}\sum_{i\in V}\sum_{j\in V}c_{ij}x^k_{ij} $$

## subject-to
For vehicle k, there is one way out of the depot and one way in.  
$\sum_{j\in V\setminus\left\\{0\right\\}} x^k_{0j}\leq 1,\\;\forall k\in K$  
$\sum_{i\in V\setminus\left\\{0\right\\}} x^k_{i0}\leq 1,\\;\forall k\in K$  
  
Only one vehicle at a customer node needs to enter and exit once.  
$\sum_{k\in K}\sum_{j\in V\setminus\left\\{i\right\\}} x^k_{ij}= 1,\\;\forall i\in V_n$  
$\sum_{k\in K}\sum_{i\in V\setminus\left\\{j\right\\}} x^k_{ij}= 1,\\;\forall j\in V_n$  
  
Incoming and outgoing vehicles must be the same at every node.  
$\sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ij} = \sum_{j\in V\setminus\left\\{i\right\\}}x^k_{ji},\\;\forall k\in K,\\;\forall i\in V$  
  
The battery or fuel of the vehicle exiting the depot is fully charged.  
$u1^k_0=Q_c,\\;\forall k\in K_c$  
$u1^k_0=Q_e,\\;\forall k\in K_e$  
  
The battery of EV exiting the charging station is fully charged.  
$u1^k_i=Q_c,\\;\forall k\in K_c,\\;\forall i\in V_c$  
  
The fuel of CV exiting the fuel station is fully charged.  
$u1^k_i=Q_e,\\;\forall k\in K_e,\\;\forall i\in V_e$  
  
EV can't go to fuel station and CV can't go to charging station  
$x^k_{ij}, x^k_{ji}=0,\\;\forall k\in K_c,\\;\forall i\in V_e,\\;\forall j\in V$  
$x^k_{ij}, x^k_{ji}=0,\\;\forall k\in K_e,\\;\forall i\in V_c,\\;\forall j\in V$  
  
The amount of fuel and charge in each car is greater than zero and less than the maximum capacity.  
$u1^k_i, u2^k_i\geq 0,\\;\forall k\in K,\\;\forall i\in V$  
$u1^k_i, u2^k_i\leq Q_c,\\;\forall k\in K_c,\\;\forall i\in V$  
$u1^k_i, u2^k_i\leq Q_e,\\;\forall k\in K_e,\\;\forall i\in V$  
  
It is a formula that represents the fuel consumption of each vehicle.  
$u1^k_i-r_cc_{ij}x^k_{ij}+Q_c(1-x^k_{ij})\geq u2^k_i,\\;\forall k\in K_c,\\;\forall i, j\in V\setminus\left\\{0\right\\}, i\neq j$  
$u1^k_i-r_ec_{ij}x^k_{ij}+Q_e(1-x^k_{ij})\geq u2^k_i,\\;\forall k\in K_e,\\;\forall i, j\in V\setminus\left\\{0\right\\}, i\neq j$  
  
It is a constraint indicating the continuity of the remaining fuel.  
$u1^k_i=u2^k_i,\\;\forall k\in K,\\;\forall i\in V$  
  
When departing from depot, the vehicle's cargo load is maximum, and the collected goods load is zero.  
$s^k_0=C_c,\\;\forall k\in K_c$  
$s^k_0=C_e,\\;\forall k\in K_e$  
$r^k_0=0,\\;\forall k\in K$  
  
The sum of the new and collected goods is less than the maximum load of each vehicle and greater than zero.  
$s^k_i+r^k_i\geq0,\\;\forall k\in K,\\;\forall i\in V$  
$s^k_i+r^k_i\leq C_c,\\;\forall k\in K_c,\\;\forall i\in V$  
$s^k_i+r^k-i\leq C_e,\\;\forall k\in K_e,\\;\forall i\in V$  
  
It is a formula representing changes in new products and changes in collected products.  
$s^k_i-d_ix^k_{ij}+C_c(1-x^k_{ij})\geq s^k_j,\\;\forall k\in K_c,\\;\forall i\in V,\\;\forall j\in V_n,\\;i\neq j$  
$s^k_i-d_ix^k_{ij}+C_e(1-x^k_{ij})\geq s^k_j,\\;\forall k\in K_e,\\;\forall i\in V,\\;\forall j\in V_n,\\;i\neq j$  
$s^k_i+C_c(1-x^k_{ij})\geq s^k_j,\\;\forall k\in K_c,\\;\forall i\in V,\\;\forall j\in V_c,\\;i\neq j$  
$s^k_i+C_e(1-x^k_{ij})\geq s^k_j,\\;\forall k\in K_e,\\;\forall i\in V,\\;\forall j\in V_e,\\;i\neq j$  
$r^k_i+p_ix^k_{ij}-C_c(1-x^k_{ij})\leq r^k_j,\\;\forall k\in K_c,\\;\forall i\in V,\\;\forall j\in V_n,\\;i\neq j$  
$r^k_i+p_ix^k_{ij}-C_e(1-x^k_{ij})\leq r^k_j,\\;\forall k\in K_e,\\;\forall i\in V,\\;\forall j\in V_n,\\;i\neq j$  
$r^k_i-C_c(1-x^k_{ij})\leq r^k_j,\\;\forall k\in K_c,\\;\forall i\in V,\\;\forall j\in V_c,\\;i\neq j$  
$r^k_i-C_e(1-x^k_{ij})\leq r^k_j,\\;\forall k\in K_e,\\;\forall i\in V,\\;\forall j\in V_e,\\;i\neq j$  
  
Constraints that remove sub-tours.  
$y^k_{i}-(n+1)x_{ij}\geq y^k_{j}-n,\\;\forall k\in K,\\;\forall i\in V\setminus\left\\{0\right\\},\\;\forall j\in V\setminus\left\\{0\right\\},\\;i\neq j$  
  
$x^k_{ij}\in \left\\{0, 1\right\\},\\;\forall i, j\in V$  

# Result Example Image

<img src=""/>
