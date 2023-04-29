from PIL import Image, ImageDraw
import mip 

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
    img.save('result image/result-EVRPMF.png')
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