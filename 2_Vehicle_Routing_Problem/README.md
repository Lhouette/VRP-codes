# FORMULATION

***Sets:*** <br/>
$V$ : sets of customer nodes <br/>
<br/>
***Parameters:*** <br/>
$c_{ij}$ : distance of traveling from node i to j <br/>
$n$ : number of customer nodes <br/>
$K$ : number of Vehicles <br/>
<br/>
***Variables:*** <br/>
$x_{ij}$ : 1 if vehicle travels from node i to j, 0 otherwise <br/>
$y_{ij}$ : variables to remove sub-tour


## Objective function
 
$$min(Z) =\sum_{i\in V}\sum_{j\in V}c_{ij}x_{ij} $$

## subject-to

$$ \sum_{j\in V\setminus\left\\{0\right\\}} x_{0j}= K $$
