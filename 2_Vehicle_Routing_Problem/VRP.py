from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY
from PIL import Image, ImageDraw
import random
from math import cos, sin, pi

# K는 vehicle의 개수
K = 1
# N은 customer node의 개수
N = 10
# (0, 0)에는 depot node
coordinates = [[0, 0]] 
# 랜덤 좌표에 20개의 customer node 생성
for i in range(N):
    #coordinates.append([20*random.random()-10, 20*random.random()-10])
    r = 7*random.random()+3
    t = random.random()
    coordinates.append([r*cos(t*2*pi), r*sin(t*2*pi)])
    #coordinates.append([r*cos(i/N*2*pi), r*sin(i/N*2*pi)])
# 각 지점으로부터의 거리 dists
dists = []
for i in range(len(coordinates)):
    dists.append([])
    for j in range(len(coordinates)-i-1):
        dists[i].append(((coordinates[i][0]-coordinates[i+j+1][0])**2+(coordinates[i][1]-coordinates[i+j+1][1])**2)**(1/2))
# node의 개수와 점의 리스트
n, V = len(dists), set(range(len(dists)))
# distances matrix
c = [[0 if i == j
      else dists[i][j-i-1] if j>i
      else dists[j][i-j-1]
      for j in V] for i in V]

model = Model()

x = [[[model.add_var(var_type=BINARY) for j in V] for i in V] for k in set(range(K))]

y = [[model.add_var() for i in V] for k in set(range(K))]

model.objective = minimize(xsum(c[i][j]*x[k][i][j] for k in set(range(K)) for i in V for j in V))
# 경로 k에 대해서 depot에서 나오는 길은 하나, 들어오는 길은 하나
for k in set(range(K)):
    model += xsum(x[k][0][j] for j in V-{0}) == 1
    model += xsum(x[k][i][0] for i in V-{0}) == 1

# 각 customer node에서 모든 경로 k를 고려해서 나가는 길은 하나
for i in V - {0}:
    model += xsum(x[k][i][j] for k in set(range(K)) for j in V - {i}) == 1
# 각 customer node에서 모든 경로 k를 고려해서 들어가는 길은 하나
for j in V - {0}:
    model += xsum(x[k][i][j] for k in set(range(K)) for i in V - {j}) == 1

for k in set(range(K)):
    for i in V - {0}:
        # k번째 경로로 들어왔으면 나가는 것도 k경로로 나간다. 
        model += xsum(x[k][i][j] for j in V - {i}) == xsum(x[k][j][i] for j in V - {i})
    # depot과 연결되지 않는 닫힌 경로 제거하는 constraints
    for (i,j) in product(V-{0}, V-{0}):
        if i != j:
            model += y[k][i] - (n+1)*x[k][i][j] >= y[k][j]-n


model.optimize()

# 그림 그려주는 코드 
amp = 5
radius = 3
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
    c = [0x000000, 0xFF0000, 0x00FF00, 0x0000FF, 0x00FFFF, 0xFFFF00, 0xFF00FF, 0x0F0F0F]
    #c = ['black', 'red', 'blue', 'green', 'cyan']
    out.write('******* route with total distance %g *******'
              % (model.objective_value))
    for k in range(K):
        route = [i for i in V - {0} if x[k][0][i].x >= 0.99][0]
        draw.line((100*amp, 
                   100*amp, 
                   (100 + 10*coordinates[route][0])*amp, 
                   (100 + 10*coordinates[route][1])*amp), 
                   fill=c[k], width=w)
        for i in V-{0}:
            r = [j for j in V - {i} if x[k][i][j].x >= 0.99]
            if len(r) == 0:
                continue
            r = r[0]
            draw.line(((100 + 10*coordinates[i][0])*amp, 
                       (100 + 10*coordinates[i][1])*amp, 
                       (100 + 10*coordinates[r][0])*amp, 
                       (100 + 10*coordinates[r][1])*amp), 
                       fill=c[k], width=w)
        
    draw.rectangle(((100-radius)*amp,
                    (100-radius)*amp,
                    (100+radius)*amp,
                    (100+radius)*amp), 
                    fill='white', outline='black', width=5)
    for i in V-{0}:
        draw.ellipse(((100 - radius + 10*coordinates[i][0])*amp, 
                      (100 - radius + 10*coordinates[i][1])*amp, 
                      (100 + radius + 10*coordinates[i][0])*amp, 
                      (100 + radius + 10*coordinates[i][1])*amp), 
                      fill="white", outline='black', width=5)
    img.show()
    img.save('result-VRP.png')
else:
    print("NO ANSWER")



