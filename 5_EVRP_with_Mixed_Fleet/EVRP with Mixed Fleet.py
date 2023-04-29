from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY
import random
from math import cos, sin, pi
import ImageMaker as IM


# N     : customer node의 개수
# Kc    : conventional vehicle의 개수
# Ke    : electric vehicle의 개수
# Sc    : fuel station의 개수
# Se    : charging station의 개수
# Qc    : conventional vehicle의 최대 연료 용량
# Qe    : electric vehicle의 최대 배터리 용량
# rc    : 거리에 따라 소모되는 연료의 양
# re    : 거리에 따라 소모되는 배터리의 양
N = 6
Kc, Ke = 2, 2
Sc, Se = 2, 2
Qc, Qe = 200, 20
rc, re = 2, 1

# (0, 0) depot node
coordinates = [[0, 0]] 

# 랜덤 좌표에 N개의 customer node 생성
for i in range(N):
    #coordinates.append([20*random.random()-10, 20*random.random()-10])
    r = 7*random.random()+3
    t = random.random()
    #r = 6.5
    #t = 1/N*(i+0.5)
    coordinates.append([r*cos(t*2*pi), r*sin(t*2*pi)])
    #coordinates.append([r*cos(i/N*2*pi), r*sin(i/N*2*pi)])

# Sc개의 fuel station
for i in range(Sc):
    r = 7.5
    t = 2*pi/Sc*(i)
    coordinates.append([r*cos(t), r*sin(t)])

# Se개의 charging station
for i in range(Se):
    r = 5.5
    t = 2*pi/Se*(i)
    coordinates.append([r*cos(t), r*sin(t)])

# 각 지점으로부터의 거리 dists
dists = []
for i in range(len(coordinates)):
    dists.append([])
    for j in range(len(coordinates)-i-1):
        dists[i].append(((coordinates[i][0]-coordinates[i+j+1][0])**2+(coordinates[i][1]-coordinates[i+j+1][1])**2)**(1/2))
# node의 개수와 점의 리스트
n, V = len(dists), set(range(len(dists)))
CS = set(range(N+1, N+M+1)) # charging station의 set
# distances matrix
c = [[0 if i == j
      else dists[i][j-i-1] if j>i
      else dists[j][i-j-1]
      for j in V] for i in V]

#==========        Formulation        ===========

model = Model()

x = [[[model.add_var(var_type=BINARY) for j in V] for i in V] for k in set(range(K))]

# depot와 연결되지 않는 닫힌 경로를 제거하기 위한 y
y = [[model.add_var() for i in V] for k in set(range(K))]

# 각 vehicle k가 i node에서 u1은 출발 배터리 양, u2는 도착 배터리 양 
u1 = [[model.add_var() for i in V] for k in set(range(K))]
u2 = [[model.add_var() for i in V] for k in set(range(K))]

# 총 이동경로의 최소화가 목적함수
model.objective = minimize(xsum(c[i][j]*x[k][i][j] for k in set(range(K)) for i in V for j in V))

# 경로 k에 대해서 depot에서 나오는 길은 하나, 들어오는 길은 하나
for k in set(range(K)):
    model += xsum(x[k][0][j] for j in V-{0}) == 1
    model += xsum(x[k][i][0] for i in V-{0}) == 1

# 각 customer node에서 모든 경로 k를 고려해서 나가는 길은 하나
for i in V - {0} - CS:
    model += xsum(x[k][i][j] for k in set(range(K)) for j in V - {i}) == 1
# 각 customer node에서 모든 경로 k를 고려해서 들어가는 길은 하나
for j in V - {0} - CS:
    model += xsum(x[k][i][j] for k in set(range(K)) for i in V - {j}) == 1
# charging station은 몇번이고 들를 수 있음
# depot에서 나가는 vehicle의 배터리는 Q
for k in set(range(K)):
    for i in CS:
        model += u1[k][i] == Q
# charging station에서 나가는 vehicle의 배터리는 Q
for k in set(range(K)):
    model += u1[k][0] == Q
# 각 시점의 배터리의 값은 0과 Q사이에 있어야 함
for k in set(range(K)):
    for i in V:
        u1[k][i] >= 0
        u1[k][i] <= Q
        u2[k][i] >= 0
        u2[k][i] <= Q
# k번째 경로로 들어왔으면 나가는 것도 k경로로 나간다. 
for k in set(range(K)):
    for i in V - {0}:
        model += xsum(x[k][i][j] for j in V - {i}) == xsum(x[k][j][i] for j in V - {i})

for k in set(range(K)):
    for (i,j) in product(V-{0}, V-{0}):
        if i != j:
            model += y[k][i] - (n+1)*x[k][i][j] >= y[k][j]-n

# 배터리의 소모
for k in set(range(K)):
    for (i, j) in product(V, V):
        if i != j:
            model += u1[k][i] - R*c[i][j]*x[k][i][j] + Q*(1 - x[k][i][j]) >= u2[k][j]
# 각 customer node에서 들어올때 배터리와 나갈때 배터리의 양은 같다. depot 제외
for k in set(range(K)):
    for i in V - {0} -CS:
        model += u1[k][i] == u2[k][i]

model.optimize()

# 그림 그려주는 코드 

    



