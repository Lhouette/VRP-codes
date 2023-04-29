from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY
from PIL import Image
import random
from math import cos, sin, pi, sqrt, dist
import ImageMaker as IM

# N     : customer node의 개수
# kc    : conventional vehicle의 개수
# ke    : electric vehicle의 개수
# Sc    : fuel station의 개수
# Se    : charging station의 개수
# Qc    : conventional vehicle의 최대 연료 용량
# Qe    : electric vehicle의 최대 배터리 용량
# rc    : 거리에 따라 소모되는 연료의 양
# re    : 거리에 따라 소모되는 배터리의 양
N = 12
kc, ke = 2, 2
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

# Sc개의 fuel station 위치 지정
for i in range(Sc):
    r = 7.5
    t = 2*pi/Sc*(i)
    coordinates.append([r*cos(t), r*sin(t)])

# Se개의 charging station 위치 지정
for i in range(Se):
    r = 5.5
    t = 2*pi/Se*(i)
    coordinates.append([r*cos(t), r*sin(t)])

# 각 지점으로부터의 거리 dists
dists = []
for i in range(len(coordinates)):
    dists.append([])
    for j in range(len(coordinates)-i-1):
        dists[i].append(dist(coordinates[i], coordinates[j]))

# =====================           Sets          ===================== 
# V     : 모든 노드의 set
# Vn    : customer node의 set
# Vc    : fuel station의 set
# Ve    : charging station의 set
V = set(range(1+N+Sc+Se))
Vn = set(range(1, 1+N))
Vc = set(range(1+N, 1+N+Sc))
Ve = set(range(1+N+Sc, 1+N+Sc+Se))
# K     : 모든 vehicle set
# Kc    : conventional vehicle set
# Ke    : electrical vehicle set
K = set(range(kc+ke))
Kc = set(range(kc))
Ke = set(range(kc, kc+ke))

# distances matrix
c = [[0 if i == j
      else dists[i][j-i-1] if j>i
      else dists[j][i-j-1]
      for j in V] for i in V]

# ===================== Parameters & Variables =====================

# n     : 노드의 총 개수
n = len(V)

model = Model()

x = [[[model.add_var(var_type=BINARY) for j in V] for i in V] for k in K]

# depot와 연결되지 않는 닫힌 경로를 제거하기 위한 y
y = [[model.add_var() for i in V] for k in K]

# 각 vehicle k가 i node에서 u1은 출발 배터리 양, u2는 도착 배터리 양 
u1 = [[model.add_var() for i in V] for k in K]
u2 = [[model.add_var() for i in V] for k in K]

# =====================   Objective Function   =====================

model.objective = minimize(xsum(c[i][j]*x[k][i][j] for k in K for i in V for j in V))

# =====================       Subject-to       =====================

# 경로 k에 대해서 depot에서 나오는 길은 하나, 들어오는 길은 하나
for k in K:
    model += xsum(x[k][0][j] for j in V-{0}) == 1
    model += xsum(x[k][i][0] for i in V-{0}) == 1

# 각 customer node에서 모든 경로 k를 고려해서 나가는 길은 하나
for i in Vn:
    model += xsum(x[k][i][j] for k in K for j in V - {i}) == 1

# 각 customer node에서 모든 경로 k를 고려해서 들어가는 길은 하나
for j in Vn:
    model += xsum(x[k][i][j] for k in K for i in V - {j}) == 1

# depot에서 나가는 vehicle의 배터리나 연료는 최대
for k in Kc:
    model += u1[k][0] == Qc
for k in Ke:
    model += u1[k][0] == Qe

# 각 충전, 주유소에서 나가는 vehicle의 배터리나 연료는 최대
for k in Kc:
    for i in Vc:
        model += u1[k][i] == Qc
for k in Ke:
    for i in Ve:
        model += u1[k][i] == Qe

# 각 시점의 배터리의 값은 0과 최댓값 사이에 있어야 함
for i in V:
    for k in Kc:
        u1[k][i] >= 0
        u1[k][i] <= Qc
        u2[k][i] >= 0
        u2[k][i] <= Qc
    for k in Ke:
        u1[k][i] >= 0
        u1[k][i] <= Qe
        u2[k][i] >= 0
        u2[k][i] <= Qe

# 모든 노드에서 vehicle k가 들어오는 수와 나가는 수는 같다. 
for k in K:
    for i in V - {0}:
        model += xsum(x[k][i][j] for j in V - {i}) == xsum(x[k][j][i] for j in V - {i})

# sub-tour를 제거하는 constraints
for k in K:
    for (i,j) in product(V-{0}, V-{0}):
        if i != j:
            model += y[k][i] - (n+1)*x[k][i][j] >= y[k][j]-n

# 연료와 배터리의 소모
for (i, j) in product(V, V):
    if i != j:
        for k in Kc:
            model += u1[k][i] - rc*c[i][j]*x[k][i][j] + Qc*(1 - x[k][i][j]) >= u2[k][j]
        for k in Ke:
            model += u1[k][i] - re*c[i][j]*x[k][i][j] + Qe*(1 - x[k][i][j]) >= u2[k][j]

# 각 customer node에서 들어올때 배터리와 나갈때 배터리의 양은 같다. depot 제외
for k in K:
    for i in Vn:
        model += u1[k][i] == u2[k][i]

# =====================       모델 풀이       =====================
model.optimize()

# =====================      이미지 생성      =====================
SIZE = 10
node_size = 4
route_width = 2

if model.num_solutions:
    out.write('******* route with total distance %g *******'%(model.objective_value))
    res_img = IM.makeresimg()
else:
    print("NO ANSWER")
    res_img = IM.makerawimg()
