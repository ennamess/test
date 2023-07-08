import rsk
import time
import math
import numpy as np
import traceback
import random
#c = rsk.Client(host = '127.0.0.1',key='')
c = rsk.Client(host='192.168.1.104',key='')
t_ref = time.time()

attaquant = input("robot gardien : ")
attaquant2 = input("robot attaquant : ")


if attaquant == "blue1":
    A = c.blue1
elif attaquant == "blue2":
    A = c.blue2
elif attaquant == "green1":
    A = c.green1
elif attaquant == "green2":
    A = c.green2
    
if attaquant2 == "blue1":
    A2 = c.blue1
elif attaquant2 == "blue2":
    A2 = c.blue2
elif attaquant2 == "green1":
    A2 = c.green1
elif attaquant2 == "green2":
    A2 = c.green2
    

K = math.copysign(1,A.position[0])



x1 = -0.2*K
y1 = random.uniform(-0.35, 0.35)
x_J2 = -1.0*K
y_J2 = random.uniform(-0.25, 0.25)
angle = 0

def angle(x,y):
    print("coor : ",x,y)
    U1 = math.sqrt((-c.ball[0]+x)**2+(c.ball[1]-y)**2)
    U2 =  x-c.ball[0]
    print("b",U1,U2,U2/U1)
    ang = math.acos(U2/U1)
    if y<c.ball[1]:
        ang = -ang
    print(ang,"angle")
    return ang

def equationD():    
    a,b= np.polyfit((x1,c.ball[0]), (y1,c.ball[1]),1)
    print(a,b)
    return a,b
    
def Y_equation(a,b,x):
    d = a*(c.ball[0]+x)+b
    return d
   

def visé(x,y):
    n = c.ball[0]-x
    n2 = c.ball[1] - y
    m = math.copysign(1, n)
    m2 = math.copysign(1, n2)
    X = m*0.04
    X2 = m*0.20
    a,b = equationD()
    d = Y_equation(a,b,X)
    d2 = d + 0.20*m2
    print("a",x,y)
    ang = angle(x,y)
    
    if ang >-2 and ang<-0.9:
        d = c.ball[1]+0.04
    elif ang <2 and ang >0.9:
        d = c.ball[1]-0.04
    return X,X2,d,d2,ang

def distance(x,y,x1,y1):
        return math.sqrt(((x1-x)**2) + ((y1-y)**2))

B1 = c.ball
x,x2,d,d2,ang = visé(x1,y1)
#    A.goto((c.ball[0]+x2,d2,0+ang))
A.goto((c.ball[0]+x,d,0+ang))
A.kick()

xx = A.position[0]+math.cos(ang)*1.3 # !!!
yy = A.position[1]+math.sin(ang)*1.3 # !!! distance de tir de 1,3



time.sleep(5)# !!! temps à changer
B2 = c.ball
x,x2,d,d2,ang = visé(x_J2,y_J2)
A2.goto((c.ball[0]+x2,d2,0+ang))
A2.goto((c.ball[0]+x,d,0+ang))
A2.goto((xx-0.05,yy,0+ang))
A2.kick()
print("-",B2,"-",xx,"-",yy)
print("--",distance(B1[0],B1[1],B2[0],B2[1]))