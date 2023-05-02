from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY
from PIL import Image, ImageDraw
import random
from math import cos, sin, pi

def drawarrow(draw, pos, color, width, amp):
    a = 30/180*pi
    dist = ((pos[0]-pos[2])**2+(pos[1]-pos[3])**2)**0.5
    midpoint = ((pos[0]+pos[2])/2, (pos[1]+pos[3])/2)
    draw.line(pos, fill=color, width=width)
    vec = (3*amp*(pos[0]-pos[2])/dist, 3*amp*(pos[1]-pos[3])/dist)
    vec1 = (vec[0]*cos(a)-vec[1]*sin(a), vec[0]*sin(a)+vec[1]*cos(a))
    pos1 = midpoint + (midpoint[0]+vec1[0], midpoint[1]+vec1[1])
    vec2 = (vec[0]*cos(a)+vec[1]*sin(a), -vec[0]*sin(a)+vec[1]*cos(a))
    pos2 = midpoint + (midpoint[0]+vec2[0], midpoint[1]+vec2[1])
    draw.line(pos1, fill=color, width=width)
    draw.line(pos2, fill=color, width=width)

# K : vehicle의 개수
# N : customer node의 개수
# M : charging station의 개수
# Q : 배터리의 최대 용량
# R : 거리에 따라 소모되는 배터리의 양
K = 2
N = 4
M = 4
Q = 20
R = 1

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
for i in range(N, N+M):
    r = 6.5
    t = 2*pi/M*(i-N)
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
# 총 이동경로의 최소화가 목적
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
        model += u1[k][i] >= 0
        model += u1[k][i] <= Q
        model += u2[k][i] >= 0
        model += u2[k][i] <= Q
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
amp = 5
radius = 4
w = 2
if model.num_solutions:
    img = Image.new(mode='RGB', size=(200*amp, 200*amp), color=0xFFFFFF)
    draw = ImageDraw.Draw(img)
    draw.ellipse((0,
                  0,
                  200*amp,
                  200*amp), 
                  fill=0xF0F0F0)
    draw.ellipse((70*amp,
                  70*amp,
                  130*amp,
                  130*amp),
                  fill=0xFFFFFF)
    co = [0x000000, 0xFF0000, 0x00FF00, 0x0000FF, 0x00FFFF, 0xFFFF00, 0xFF00FF, 0x0F0F0F]
    #c = ['black', 'red', 'blue', 'green', 'cyan']
    out.write('******* route with total distance %g *******'
              % (model.objective_value))
    bat = []
    for i in V:
        bat.append(Q)
    for k in range(K):
        cp = 0
        while(True):
            np = [i for i in V if x[k][cp][i].x >= 0.99][0]
            bat[np] = bat[cp] - c[cp][np]*R
            if np in CS:
                bat[np] = Q
            cp = np
            if cp == 0:
                bat[0] = Q
                break
        route = [i for i in V - {0} if x[k][0][i].x >= 0.99][0]
        pos = (100*amp, 
               100*amp, 
               (100 + 10*coordinates[route][0])*amp, 
               (100 + 10*coordinates[route][1])*amp)
        drawarrow(draw, pos, co[k], w, amp)
        """
        draw.line((100*amp, 
                   100*amp, 
                   (100 + 10*coordinates[route][0])*amp, 
                   (100 + 10*coordinates[route][1])*amp), 
                   fill=c[k], width=w)"""
        
        for i in V-{0}:
            r = [j for j in V - {i} if x[k][i][j].x >= 0.99]
            if len(r) == 0:
                continue
            r = r[0]
            pos = ((100 + 10*coordinates[i][0])*amp, 
                   (100 + 10*coordinates[i][1])*amp, 
                   (100 + 10*coordinates[r][0])*amp, 
                   (100 + 10*coordinates[r][1])*amp)
            drawarrow(draw, pos, co[k], w, amp)
        
    draw.rectangle(((100-radius)*amp,
                    (100-radius)*amp,
                    (100+radius)*amp,
                    (100+radius)*amp), 
                    fill='white', outline='black', width=5)
    for i in V-{0}-CS:
        pos = ((100 - radius + 10*coordinates[i][0])*amp, 
               (100 - radius + 10*coordinates[i][1])*amp, 
               (100 + radius + 10*coordinates[i][0])*amp, 
               (100 + radius + 10*coordinates[i][1])*amp)
        draw.ellipse(pos, fill="white", outline='black', width=5)
        battext = "{:.1f}".format(bat[i])
        w, h = draw.textsize(battext)
        draw.text(((100+10*coordinates[i][0])*amp-w/2, 
                   (100+10*coordinates[i][1])*amp-h/2), battext, fill='black')
    for i in CS:
        pos = ((100 - radius + 10*coordinates[i][0])*amp, 
               (100 - radius + 10*coordinates[i][1])*amp, 
               (100 + radius + 10*coordinates[i][0])*amp, 
               (100 + radius + 10*coordinates[i][1])*amp)
        draw.ellipse(pos, fill="white", outline='GREEN', width=5)
    img.show()
    img.save('result-EVRP.png')
else:
    print("NO ANSWER")
    img = Image.new(mode='RGB', size=(200*amp, 200*amp), color=0xFFFFFF)
    draw = ImageDraw.Draw(img)
    draw.ellipse((0,
                  0,
                  200*amp,
                  200*amp), 
                  fill=0xF0F0F0)
    draw.ellipse((70*amp,
                  70*amp,
                  130*amp,
                  130*amp),
                  fill=0xFFFFFF)
    draw.rectangle(((100-radius)*amp,
                    (100-radius)*amp,
                    (100+radius)*amp,
                    (100+radius)*amp), 
                    fill='white', outline='black', width=5)
    for i in V-{0}-CS:
        draw.ellipse(((100 - radius + 10*coordinates[i][0])*amp, 
                      (100 - radius + 10*coordinates[i][1])*amp, 
                      (100 + radius + 10*coordinates[i][0])*amp, 
                      (100 + radius + 10*coordinates[i][1])*amp), 
                      fill="white", outline='black', width=5)
    for i in CS:
        draw.ellipse(((100 - radius + 10*coordinates[i][0])*amp, 
                      (100 - radius + 10*coordinates[i][1])*amp, 
                      (100 + radius + 10*coordinates[i][0])*amp, 
                      (100 + radius + 10*coordinates[i][1])*amp), 
                      fill="white", outline='GREEN', width=5)
    img.show()
    



