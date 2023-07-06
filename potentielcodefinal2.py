#potentielcodefinal2

import rsk
import time
import math
import numpy as np
import traceback
import random
# couleur = str(input("Quelle couleur : "))
cote = str(input("Quel côté : "))
c = rsk.Client(host='127.0.0.1',key='')
t_ref=time.time()



def update():
    position_robots()
    position_balle()
    distances()

if cote == 'g':
    def position_robots():
                    global xg1, yg1, xg2, yg2, xb1, yb1, xb2, yb2
                
                    xg1 = c.blue1.position[0]
                    yg1 = c.blue1.position[1]
                    xg2 = c.blue2.position[0]
                    yg2 = c.blue2.position[1]
                    xb1 = c.blue1.position[0]
                    yb1 = c.blue1.position[1]
                    xb2 = c.blue2.position[0]
                    yb2 = c.blue2.position[1]

                    return xg1, yg1, xg2, yg2, xb1, yb1, xb2, yb2

    def position_balle():
        global xb, yb
    
        xb = c.ball[0]
        yb = c.ball[1]
        return xb, yb
    


    def distances():
        global dg1, dg2, db1, db2
        # Avoir la distance entre les robots et la balle
        dg1 = math.sqrt(((xg1 - xb)**2) + ((yg1 - yb)**2))
        dg2 = math.sqrt(((xg2 - xb)**2) + ((yg2 - yb)**2))
        db1 = math.sqrt(((xb1 - xb)**2) + ((yb1 - yb)**2))
        db2 = math.sqrt(((xb2 - xb)**2) + ((yb2 - yb)**2))

    def position_depart():
        c.blue1.goto((0.8, 0, 0.))

    def tir():
        global t_ref
        
        y1 = random.uniform(-0.25,0.25)
        t1 = time.time()
        
        update()
        if t1>=t_ref+1:
            c.blue1.kick()
            t_ref=t1

    def tir2():
        c.blue2.kick()

    def y_Attack_a_gauche(y1):
            x=[]
            y=[]
            x.append(c.ball[0])
            y.append(c.ball[1])
            x.append(1)#!!!!!
            y.append(y1)
            a,b = np.polyfit(x, y, 1)
            if y[1] > y[0]:
                a = -abs(a)
            else:
                a = abs(a)
            y_Axe = a*0.45+b
            return y_Axe
    
    def distance(x,y,x1,y1):
        return math.sqrt(((x1-x)**2) + ((y1-y)**2)) #Distance entre 2 point avec pythagore

    def y_cage():
        y1 = random.uniform(-0.25,0.25)
        return y1
    
    def distance2(y1):
            U2=distance(c.ball[0],c.ball[1],-1,y1)
            U1=distance(c.ball[0],c.ball[1],-1,c.ball[1])
            cos=math.acos(U1/U2)
            return cos #Calcul orientation robot dois prendre
    
    def distance_balle_robot1():
        return(distance(c.blue1.position[0],c.blue1.position[1],c.ball[0],c.ball[1])) #distance robot green 1 et la balle

    def positionnement1(y1,cos, y_Axe):
        if y1 >= c.ball[1]:
            c.blue1.goto((c.ball[0] + 0.1, y_Axe, math.pi - cos))  # le robot se positionne sur la droite (y)
            c.blue1.goto((c.ball[0], c.ball[1], math.pi - cos))  # le robot avance a la balle
        else:
            c.blue1.goto((c.ball[0] + 0.1, y_Axe, math.pi + cos))  # le robot se positionne sur la droite (y)
            c.blue1.goto((c.ball[0], c.ball[1], math.pi + cos)) #le robot avance a la balle


    def y_gardien():
        global y_goal
        x=[]
        y=[]
        x.append(xb)
        x.append(xr)
        y.append(yb)
        y.append(yr)

        a,b=np.polyfit(x,y,1)[0],np.polyfit(x,y,1)[1]
        y_goal=a*0.8+b

    
    


    def gardien():
        global xr,yr
        update()
        if db1>db2:
            xr=xb2
            yr=yb2
        if db1<=db2:
            xr=xb1
            yr=yb1
        y_gardien()
        if -0.25<= y_goal <= 0.25:
            c.blue2.goto((0.8, y_goal, math.pi))
        if y_goal>0:
            c.blue2.goto((0.8, yb/2, math.pi))

        if abs(xg2 - xb) <= 0.15 and abs(yg2 - yb) <= 0.15:
            tir2()

    def kick1(t_ref):
            
            t = time.time()  # prendre temps au kick
            if t >= t_ref+1 :
                c.blue1.kick()

    def recule(y1,cos):
        if y1>=c.ball[1] :
            c.blue1.goto((c.blue1.position[0]-0.2,c.blue1.position[1], math.pi-cos), wait = True) #!!!!!!!!!!!!!!!!!!!! + -> -   #fait reculer le robot pout le sortir de la zone rouge autour de la balle
        else :
            c.blue1.goto((c.blue1.position[0]-0.2 ,c.blue1.position[1], math.pi+cos), wait = True)#!!!!!!!!!!!!!!!!!!! + -> -    fait reculer le robot pout le sortir de la zone rouge autour de la balle

    def sortie_de_terrain():
        if c.blue1.position[0]>1:
            c.blue1.goto(c.blue1.position[0]-0.1 ,c.blue1.position[1])
        elif c.blue1.position[0] < -1:
            c.blue1.goto(c.blue1.position[0]+0.1 ,c.blue1.position[1])
        elif c.blue1.position[1] < -1:
            c.blue1.goto(c.blue1.position[0], c.blue1.position[1]+0.1)
        elif c.blue1.position[1] > 1:
            c.blue1.goto(c.blue1.position[0], c.blue1.position[1]-0.1)


    def attaquant():
        global t_ref
        d=distance_balle_robot1()#créer variable "d" prennant la distance robot green 1 et balle
        y1 = y_cage()
        y_Axe = y_Attack_a_gauche(y1)
        cos = distance2(y1)
        while d >= 0.11:  # si d <0.11 le robot est a distance pour tirer
            positionnement1(y1,cos, y_Axe)
            d=distance(c.blue1.position[0],c.blue1.position[1],c.ball[0],c.ball[1]) #actualiser "d"
        kick1(t_ref)
        t_ref = time.time()  # créer un timer de 1 sec entre chaque kick
        recule(y1,cos)
        sortie_de_terrain()

    def contourner2():
        update()
        if yb-0.3 >= yg1 and yb+0.3 <= yg1:
            if yb>0:
                update()
                c.blue1.goto((xg1  , yg1 +0.25, math.pi))
            else:
                update()
                c.blue1.goto((xg1  , yg1-0.25, math.pi))


    def placement():
        update()
        contourner2()
        update()
        c.blue1.goto((xb+0.02 , yb, math.pi))

    def angle() :
        global a_br, a_b
        a_b = math.atan(yb/xb)
        a_r = math.atan(yb1/xb1)
        a_br = a_b - a_r

    def placement2() :
        contourner2()
        global p
        p = 0
        if yb > 0 :
            p = 0,15
        if yb < 0 :
            p = -0,15
        else :
            pass
        c.blue1.goto(xb - 0.15, yb + p, a_b - (math.pi)/2)
    
    

    while True:
        try:
            
            update()
            gardien()
            update()
            attaquant()
            

        except BaseException as t:
            print("Il y a une erreur: ")
            print(t)
            print(traceback.format_exc())
            pass
    
else :

    def position_robots():
                    global xg1, yg1, xg2, yg2, xb1, yb1, xb2, yb2
                
                    xg1 = c.blue1.position[0]
                    yg1 = c.blue1.position[1]
                    xg2 = c.blue2.position[0]
                    yg2 = c.blue2.position[1]
                    xb1 = c.blue1.position[0]
                    yb1 = c.blue1.position[1]
                    xb2 = c.blue2.position[0]
                    yb2 = c.blue2.position[1]

                    return xg1, yg1, xg2, yg2, xb1, yb1, xb2, yb2

    def position_balle():
        global xb, yb
    
        xb = c.ball[0]
        yb = c.ball[1]
        return xb, yb
    


    def distances():
        global dg1, dg2, db1, db2
        # Avoir la distance entre les robots et la balle
        dg1 = math.sqrt(((xg1 - xb)**2) + ((yg1 - yb)**2))
        dg2 = math.sqrt(((xg2 - xb)**2) + ((yg2 - yb)**2))
        db1 = math.sqrt(((xb1 - xb)**2) + ((yb1 - yb)**2))
        db2 = math.sqrt(((xb2 - xb)**2) + ((yb2 - yb)**2))

    def position_depart():
        c.blue1.goto((0.8, 0, 0.))

    def tir():
        global t_ref
        
        y1 = random.uniform(-0.25,0.25)
        t1 = time.time()
        
        update()
        if t1>=t_ref+1:
            c.blue1.kick()
            t_ref=t1

    def tir2():
        c.blue2.kick()

    def y_Attack_a_droite(y1):
            x=[]
            y=[]
            x.append(c.ball[0])
            y.append(c.ball[1])
            x.append(-1)#!!!!
            y.append(y1)
            a,b = np.polyfit(x, y, 1)
            if y[1] > y[0]:
                a = abs(a)
            else:
                a = -abs(a)
            y_Axe = a*0.45+b
            return y_Axe
    
    def distance(x,y,x1,y1):
        return math.sqrt(((x1-x)**2) + ((y1-y)**2)) #Distance entre 2 point avec pythagore

    def y_cage():
        y1 = random.uniform(-0.25,0.25)
        return y1
    
    def distance2(y1):
            U2=distance(c.ball[0],c.ball[1],-1,y1)
            U1=distance(c.ball[0],c.ball[1],-1,c.ball[1])
            cos=math.acos(U1/U2)
            return cos #Calcul orientation robot dois prendre
    
    def distance_balle_robot1():
        return(distance(c.blue1.position[0],c.blue1.position[1],c.ball[0],c.ball[1])) #distance robot green 1 et la balle

    def positionnement1(y1,cos, y_Axe):
        if y1 >= c.ball[1]:
            c.blue1.goto((c.ball[0] - 0.1, y_Axe, 0 - cos))  # le robot se positionne sur la droite (y)
            c.blue1.goto((c.ball[0], c.ball[1], 0 - cos))  # le robot avance a la balle
        else:
            c.blue1.goto((c.ball[0] - 0.1, y_Axe, 0 + cos))  # le robot se positionne sur la droite (y)
            c.blue1.goto((c.ball[0], c.ball[1], 0 + cos)) #le robot avance a la balle


    def y_gardien():
        global y_goal
        x=[]
        y=[]
        x.append(xb)
        x.append(xr)
        y.append(yb)
        y.append(yr)

        a,b=np.polyfit(x,y,1)[0],np.polyfit(x,y,1)[1]
        y_goal=a*0.8+b

    
    


    def gardien():
        global xr,yr
        update()
        if db1>db2:
            xr=xb2
            yr=yb2
        if db1<=db2:
            xr=xb1
            yr=yb1
        y_gardien()
        if -0.25<= y_goal <= 0.25:
            c.blue2.goto((-0.8, y_goal, 0.))
        if y_goal>0:
            c.blue2.goto((-0.8, yb/2, 0.))

        if abs(xg2 - xb) <= 0.15 and abs(yg2 - yb) <= 0.15:
            tir2()

    def kick1(t_ref):
            
            t = time.time()  # prendre temps au kick
            if t >= t_ref+1 :
                c.blue1.kick()

    def recule(y1,cos):
        if y1>=c.ball[1] :
            c.blue1.goto((c.blue1.position[0]-0.2,c.blue1.position[1], 0)) #!!!!!!!!!!!!!!!!!!!! + -> -   #fait reculer le robot pout le sortir de la zone rouge autour de la balle
        else :
            c.blue1.goto((c.blue1.position[0]-0.2 ,c.blue1.position[1], 0))#!!!!!!!!!!!!!!!!!!! + -> -    fait reculer le robot pout le sortir de la zone rouge autour de la balle

    def sortie_de_terrain():
        if c.blue1.position[0]>1:
            c.blue1.goto(c.blue1.position[0]-0.1 ,c.blue1.position[1])
        elif c.blue1.position[0] < -1:
            c.blue1.goto(c.blue1.position[0]+0.1 ,c.blue1.position[1])
        elif c.blue1.position[1] < -1:
            c.blue1.goto(c.blue1.position[0], c.blue1.position[1]+0.1)
        elif c.blue1.position[1] > 1:
            c.blue1.goto(c.blue1.position[0], c.blue1.position[1]-0.1)


    def attaquant():
        global t_ref
        d=distance_balle_robot1()#créer variable "d" prennant la distance robot green 1 et balle
        y1 = y_cage()
        y_Axe = y_Attack_a_droite(y1)
        cos = distance2(y1)
        while d >= 0.11:  # si d <0.11 le robot est a distance pour tirer
            positionnement1(y1,cos, y_Axe)
            d=distance(c.blue1.position[0],c.blue1.position[1],c.ball[0],c.ball[1]) #actualiser "d"
        kick1(t_ref)
        t_ref = time.time()  # créer un timer de 1 sec entre chaque kick
        recule(y1,cos)
        sortie_de_terrain()

    def contourner2():
        update()
        if yb-0.3 >= yg1 and yb+0.3 <= yg1:
            if yb>0:
                update()
                c.blue1.goto((xg1  , yg1 +0.25, math.pi))
            else:
                update()
                c.blue1.goto((xg1  , yg1-0.25, math.pi))


    def placement():
        update()
        contourner2()
        update()
        c.blue1.goto((xb+0.02 , yb, math.pi))

    def angle() :
        global a_br, a_b
        a_b = math.atan(yb/xb)
        a_r = math.atan(yb1/xb1)
        a_br = a_b - a_r

    def placement2() :
        contourner2()
        global p
        p = 0
        if yb > 0 :
            p = 0,15
        if yb < 0 :
            p = -0,15
        else :
            pass
        c.blue1.goto(xb - 0.15, yb + p, a_b - (math.pi)/2)
    
    

    while True:
        try:
            
            update()
            gardien()
            update()
            attaquant()
            

        except BaseException as t:
            print("Il y a une erreur: ")
            print(t)
            print(traceback.format_exc())
            pass
    