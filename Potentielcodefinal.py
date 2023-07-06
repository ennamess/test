import random
from turtle import position
import rsk
import time
import math
import numpy as np
import traceback
c = rsk.Client(host='192.168.0.102' , key='ss9vyp')
t_ref=time.time()      #Actualiser le temps ref au début de la partie
import traceback
couleur = str(input("Quelle couleur : "))
cote = str(input("Quel côté : "))


if couleur=='g':
    if cote=='g':
        def y_cage():
            y1 = random.uniform(-0.25,0.25)
            return y1

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

        def distance2(y1):
            U2=distance(c.ball[0],c.ball[1],-1,y1)
            U1=distance(c.ball[0],c.ball[1],-1,c.ball[1])
            cos=math.acos(U1/U2)
            return cos #Calcul orientation robot dois prendre

        def distance_balle_robot1():
            return(distance(c.green1.position[0],c.green1.position[1],c.ball[0],c.ball[1])) #distance robot green 1 et la balle
        d=distance_balle_robot1()#créer variable "d" prennant la distance robot green 1 et balle



        def positionnement1(y1,cos):
            if y1 >= c.ball[1]:
                c.green1.goto((c.ball[0] - 0.23, y_Axe, math.pi - cos))  # le robot se positionne sur la droite (y)
                c.green1.goto((c.ball[0], c.ball[1], math.pi - cos))  # le robot avance a la balle
            else:
                c.green1.goto((c.ball[0] - 0.23, y_Axe, math.pi + cos))  # le robot se positionne sur la droite (y)
                c.green1.goto((c.ball[0], c.ball[1], math.pi + cos)) #le robot avance a la balle

        def kick1(t_ref):
            t = time.time()  # prendre temps au kick
            if t >= t_ref+1 :
                c.green1.kick()

        def recule(y1,cos):
            if y1>=c.ball[1] :
                c.green1.goto((c.green1.position[0]+0.037,c.green1.position[1], math.pi-cos), wait = True) #!!!!!!!!!!!!!!!!!!!! + -> -   #fait reculer le robot pout le sortir de la zone rouge autour de la balle
            else :
                c.green1.goto((c.green1.position[0]+0.037 ,c.green1.position[1], math.pi+cos), wait = True)#!!!!!!!!!!!!!!!!!!! + -> -    fait reculer le robot pout le sortir de la zone rouge autour de la balle


        def sortie_de_terrain():
            if c.green1.position[0]>1:
                c.green1.goto(c.green1.position[0]-0.1 ,c.green1.position[1])
            elif c.green1.position[0] < -1:
                c.green1.goto(c.green1.position[0]+0.1 ,c.green1.position[1])
            elif c.green1.position[1] < -1:
                c.green1.goto(c.green1.position[0], c.green1.position[1]+0.1)
            elif c.green1.position[1] > 1:
                c.green1.goto(c.green1.position[0], c.green1.position[1]-0.1)

        y1 = y_cage()


        def distance(x, y, x1, y1):

            return math.sqrt(((x1 - x) ** 2) + ((y1 - y) ** 2))  # Distance entre 2 point avec pythagore


        def distance_balle_robot1():
            return (distance(c.green2.position[0], c.green2.position[1], c.ball[0],c.ball[1]))  # distance robot green 1 et la balle


        def position_robots_adversaire():
            xb1 = c.blue1.position[0]
            yb1 = c.blue1.position[1]
            xb2 = c.blue2.position[0]
            yb2 = c.blue2.position[1]
            return xb1, yb1, xb2, yb2


        def distances_balle_adversaire(xb1, yb1, xb2, yb2):
            db1 = math.sqrt(((xb1 - c.ball[0]) ** 2) + ((yb1 - c.ball[1]) ** 2))
            db2 = math.sqrt(((xb2 - c.ball[0]) ** 2) + ((yb2 - c.ball[1]) ** 2))
            return db1,db2

        def attaquant_adverse(db1,db2):
            coor = position_robots_adversaire()
            d = distances_balle_adversaire(coor[0],coor[1],coor[2],coor[3])
            if db1 > db2:
                xr = xb2
                yr = yb2
            if db1 <= db2:
                xr = xb1
                yr = yb1
            return xr,yr


        def y_gardien(db1,db2):
            xr,yr=attaquant_adverse(db1,db2)
            x = []
            y = []
            x.append(c.ball[0])
            x.append(xr)
            y.append(c.ball[1])
            y.append(yr)
            a, b = np.polyfit(x, y, 1)[0], np.polyfit(x, y, 1)[1]
            y_goal = a * 0.8 + b
            return y_goal

        def gardien(db1,db2):
            y_goal=y_gardien(db1, db2)
            c.green2.goto(c.green2.position[0], y_goal)

        while True:
            try:
                xb1, yb1, xb2, yb2 = position_robots_adversaire()
                db1,db2 = distances_balle_adversaire(xb1, yb1, xb2, yb2)
                gardien(db1, db2)
                y_Axe = y_Attack_a_gauche(y1)
                cos = distance2(y1)
                while d >= 0.11:  # si d <0.11 le robot est a distance pour tirer
                    positionnement1(y1,cos)
                    d=distance(c.green1.position[0],c.green1.position[1],c.ball[0],c.ball[1]) #actualiser "d"
                kick1(t_ref)
                t_ref = time.time()  # créer un timer de 1 sec entre chaque kick
                recule(y1,cos)
                #sortie_de_terrain()
                
            except BaseException as t:
                        print("Il y a une erreur: ")
                        print(t)
                        print(traceback.format_exc())
                        pass  
        

        
        def stop():
            c.green1.goto((c.green1.position[0], c.green1.position[1], math.pi), wait = False) # stop le robot a sa position actuelle.

        stop()

           
    if cote=="d":
        def y_cage():
            y1 = random.uniform(-0.25,0.25)
            return y1

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

        def distance2(y1):
            U2=distance(c.ball[0],c.ball[1],-1,y1)
            U1=distance(c.ball[0],c.ball[1],-1,c.ball[1])
            cos=math.acos(U1/U2)
            return cos #Calcul orientation robot dois prendre

        def distance_balle_robot1():
            return(distance(c.green1.position[0],c.green1.position[1],c.ball[0],c.ball[1])) #distance robot green 1 et la balle
        d=distance_balle_robot1()#créer variable "d" prennant la distance robot green 1 et balle



        def positionnement1(y1,cos):
            if y1 >= c.ball[1]:
                c.green1.goto((c.ball[0] + 0.23, y_Axe, math.pi - cos))  # le robot se positionne sur la droite (y)
                c.green1.goto((c.ball[0], c.ball[1], math.pi - cos))  # le robot avance a la balle
            else:
                c.green1.goto((c.ball[0] + 0.23, y_Axe, math.pi + cos))  # le robot se positionne sur la droite (y)
                c.green1.goto((c.ball[0], c.ball[1], math.pi + cos)) #le robot avance a la balle

        def kick1(t_ref):
            t = time.time()  # prendre temps au kick
            if t >= t_ref+1 :
                c.green1.kick()

        def recule(y1,cos):
            if y1>=c.ball[1] :
                c.green1.goto((c.green1.position[0]-0.037,c.green1.position[1], math.pi-cos), wait = True) #!!!!!!!!!!!!!!!!!!!! + -> -   #fait reculer le robot pout le sortir de la zone rouge autour de la balle
            else :
                c.green1.goto((c.green1.position[0]-0.037 ,c.green1.position[1], math.pi+cos), wait = True)#!!!!!!!!!!!!!!!!!!! + -> -    fait reculer le robot pout le sortir de la zone rouge autour de la balle


        def sortie_de_terrain():
            if c.green1.position[0]>1:
                c.green1.goto(c.green1.position[0]-0.1 ,c.green1.position[1])
            elif c.green1.position[0] < -1:
                c.green1.goto(c.green1.position[0]+0.1 ,c.green1.position[1])
            elif c.green1.position[1] < -1:
                c.green1.goto(c.green1.position[0], c.green1.position[1]+0.1)
            elif c.green1.position[1] > 1:
                c.green1.goto(c.green1.position[0], c.green1.position[1]-0.1)

        y1 = y_cage()
        def distance(x, y, x1, y1):
            return math.sqrt(((x1 - x) ** 2) + ((y1 - y) ** 2))  # Distance entre 2 point avec pythagore


        def distance_balle_robot1():
            return (distance(c.green2.position[0], c.green2.position[1], c.ball[0],c.ball[1]))  # distance robot green 1 et la balle


        def position_robots_adversaire():
            xb1 = c.blue1.position[0]
            yb1 = c.blue1.position[1]
            xb2 = c.blue2.position[0]
            yb2 = c.blue2.position[1]
            return xb1, yb1, xb2, yb2


        def distances_balle_adversaire(xb1, yb1, xb2, yb2):
            db1 = math.sqrt(((xb1 - c.ball[0]) ** 2) + ((yb1 - c.ball[1]) ** 2))
            db2 = math.sqrt(((xb2 - c.ball[0]) ** 2) + ((yb2 - c.ball[1]) ** 2))
            return db1,db2

        def attaquant_adverse(db1,db2):
            coor = position_robots_adversaire()
            d = distances_balle_adversaire(coor[0],coor[1],coor[2],coor[3])
            if db1 > db2:
                xr = xb2
                yr = yb2
            if db1 <= db2:
                xr = xb1
                yr = yb1
            return xr,yr


        def y_gardien(db1,db2):
            xr,yr=attaquant_adverse(db1,db2)
            x = []
            y = []
            x.append(c.ball[0])
            x.append(xr)
            y.append(c.ball[1])
            y.append(yr)
            a, b = np.polyfit(x, y, 1)[0], np.polyfit(x, y, 1)[1]
            y_goal = a * 0.8 + b
            return y_goal

        def gardien(db1,db2):
            y_goal=y_gardien(db1, db2)
            c.green2.goto(c.green2.position[0], y_goal)

        while True:
            try:
                xb1, yb1, xb2, yb2 = position_robots_adversaire()
                db1,db2 = distances_balle_adversaire(xb1, yb1, xb2, yb2)
                gardien(db1, db2)
                y_Axe = y_Attack_a_gauche(y1)
                cos = distance2(y1)
                while d >= 0.11:  # si d <0.11 le robot est a distance pour tirer
                    positionnement1(y1,cos)
                    d=distance(c.green1.position[0],c.green1.position[1],c.ball[0],c.ball[1]) #actualiser "d"
                kick1(t_ref)
                t_ref = time.time()  # créer un timer de 1 sec entre chaque kick
                recule(y1,cos)
                sortie_de_terrain()
            except BaseException as t:
                        print("Il y a une erreur: ")
                        print(t)
                        print(traceback.format_exc())
                        pass
        

                        
        def stop():
            c.green1.goto((c.green1.position[0], c.green1.position[1], math.pi), wait = False) # stop le robot a sa position actuelle.

        stop()






if couleur=="b":
    if cote=="d":
        def y_cage():
            y1 = random.uniform(-0.25,0.25)
            return y1

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

        def distance2(y1):
            U2=distance(c.ball[0],c.ball[1],-1,y1)
            U1=distance(c.ball[0],c.ball[1],-1,c.ball[1])
            cos=math.acos(U1/U2)
            return cos #Calcul orientation robot dois prendre

        def distance_balle_robot1():
            return(distance(c.blue1.position[0],c.blue1.position[1],c.ball[0],c.ball[1])) #distance robot green 1 et la balle
        d=distance_balle_robot1()#créer variable "d" prennant la distance robot green 1 et balle



        def positionnement1(y1,cos):
            if y1 >= c.ball[1]:
                c.blue1.goto((c.ball[0] + 0.23, y_Axe, math.pi - cos))  # le robot se positionne sur la droite (y)
                c.blue1.goto((c.ball[0], c.ball[1], math.pi - cos))  # le robot avance a la balle
            else:
                c.blue1.goto((c.ball[0] + 0.23, y_Axe, math.pi + cos))  # le robot se positionne sur la droite (y)
                c.blue1.goto((c.ball[0], c.ball[1], math.pi + cos)) #le robot avance a la balle

        def kick1(t_ref):
            t = time.time()  # prendre temps au kick
            if t >= t_ref+1 :
                c.blue1.kick()

        def recule(y1,cos):
            if y1>=c.ball[1] :
                c.blue1.goto((c.blue1.position[0]-0.037,c.blue1.position[1], math.pi-cos), wait = True) #!!!!!!!!!!!!!!!!!!!! + -> -   #fait reculer le robot pout le sortir de la zone rouge autour de la balle
            else :
                c.blue1.goto((c.blue1.position[0]-0.037 ,c.blue1.position[1], math.pi+cos), wait = True)#!!!!!!!!!!!!!!!!!!! + -> -    fait reculer le robot pout le sortir de la zone rouge autour de la balle


        def sortie_de_terrain():
            if c.blue1.position[0]>1:
                c.blue1.goto(c.blue1.position[0]-0.1 ,c.blue1.position[1])
            elif c.blue1.position[0] < -1:
                c.blue1.goto(c.blue1.position[0]+0.1 ,c.blue1.position[1])
            elif c.blue1.position[1] < -1:
                c.blue1.goto(c.blue1.position[0], c.blue1.position[1]+0.1)
            elif c.blue1.position[1] > 1:
                c.blue1.goto(c.blue1.position[0], c.blue1.position[1]-0.1)

        y1 = y_cage()
        def distance(x, y, x1, y1):
            return math.sqrt(((x1 - x) ** 2) + ((y1 - y) ** 2))  # Distance entre 2 point avec pythagore


        def distance_balle_robot1():
            return (distance(c.blue2.position[0], c.blue2.position[1], c.ball[0],c.ball[1]))  # distance robot green 1 et la balle


        def position_robots_adversaire():
            xb1 = c.green1.position[0]
            yb1 = c.green1.position[1]
            xb2 = c.green2.position[0]
            yb2 = c.green2.position[1]
            return xb1, yb1, xb2, yb2


        def distances_balle_adversaire(xb1, yb1, xb2, yb2):
            db1 = math.sqrt(((xb1 - c.ball[0]) ** 2) + ((yb1 - c.ball[1]) ** 2))
            db2 = math.sqrt(((xb2 - c.ball[0]) ** 2) + ((yb2 - c.ball[1]) ** 2))
            return db1,db2

        def attaquant_adverse(db1,db2):
            coor = position_robots_adversaire()
            d = distances_balle_adversaire(coor[0],coor[1],coor[2],coor[3])
            if db1 > db2:
                xr = xb2
                yr = yb2
            if db1 <= db2:
                xr = xb1
                yr = yb1
            return xr,yr


        def y_gardien(db1,db2):
            xr,yr=attaquant_adverse(db1,db2)
            x = []
            y = []
            x.append(c.ball[0])
            x.append(xr)
            y.append(c.ball[1])
            y.append(yr)
            a, b = np.polyfit(x, y, 1)[0], np.polyfit(x, y, 1)[1]
            y_goal = a * 0.8 + b
            return y_goal

        def gardien(db1,db2):
            y_goal=y_gardien(db1, db2)
            c.blue2.goto(c.blue2.position[0], y_goal)

        while True:
            try:
                xb1, yb1, xb2, yb2 = position_robots_adversaire()
                db1,db2 = distances_balle_adversaire(xb1, yb1, xb2, yb2)
                gardien(db1, db2)
                y_Axe = y_Attack_a_gauche(y1)
                cos = distance2(y1)
                while d >= 0.11:  # si d <0.11 le robot est a distance pour tirer
                    positionnement1(y1,cos)
                    d=distance(c.blue1.position[0],c.blue1.position[1],c.ball[0],c.ball[1]) #actualiser "d"
                kick1(t_ref)
                t_ref = time.time()  # créer un timer de 1 sec entre chaque kick
                recule(y1,cos)
                sortie_de_terrain()
            except BaseException as t:
                        print("Il y a une erreur: ")
                        print(t)
                        print(traceback.format_exc())
                        pass








       


                
    if cote=="g":
        def y_cage():
            y1 = random.uniform(-0.25,0.25)
            return y1

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

        def distance2(y1):
            U2=distance(c.ball[0],c.ball[1],-1,y1)
            U1=distance(c.ball[0],c.ball[1],-1,c.ball[1])
            cos=math.acos(U1/U2)
            return cos #Calcul orientation robot dois prendre

        def distance_balle_robot1():
            return(distance(c.blue1.position[0],c.blue1.position[1],c.ball[0],c.ball[1])) #distance robot green 1 et la balle
        d=distance_balle_robot1()#créer variable "d" prennant la distance robot green 1 et balle



        def positionnement1(y1,cos):
            if y1 >= c.ball[1]:
                c.blue1.goto((c.ball[0] - 0.23, y_Axe, math.pi - cos))  # le robot se positionne sur la droite (y)
                c.blue1.goto((c.ball[0], c.ball[1], math.pi - cos))  # le robot avance a la balle
            else:
                c.blue1.goto((c.ball[0] - 0.23, y_Axe, math.pi + cos))  # le robot se positionne sur la droite (y)
                c.blue1.goto((c.ball[0], c.ball[1], math.pi + cos)) #le robot avance a la balle

        def kick1(t_ref):
            t = time.time()  # prendre temps au kick
            if t >= t_ref+1 :
                c.blue1.kick()

        def recule(y1,cos):
            if y1>=c.ball[1] :
                c.blue1.goto((c.blue1.position[0]+0.037,c.blue1.position[1], math.pi-cos), wait = True) #!!!!!!!!!!!!!!!!!!!! + -> -   #fait reculer le robot pout le sortir de la zone rouge autour de la balle
            else :
                c.blue1.goto((c.blue1.position[0]+0.037 ,c.blue1.position[1], math.pi+cos), wait = True)#!!!!!!!!!!!!!!!!!!! + -> -    fait reculer le robot pout le sortir de la zone rouge autour de la balle


        def sortie_de_terrain():
            if c.blue1.position[0]>1:
                c.blue1.goto(c.blue1.position[0]-0.1 ,c.blue1.position[1])
            elif c.blue1.position[0] < -1:
                c.blue1.goto(c.blue1.position[0]+0.1 ,c.blue1.position[1])
            elif c.blue1.position[1] < -1:
                c.blue1.goto(c.blue1.position[0], c.blue1.position[1]+0.1)
            elif c.blue1.position[1] > 1:
                c.blue1.goto(c.blue1.position[0], c.blue1.position[1]-0.1)

        y1 = y_cage()

        def distance_balle_robot1():
            return (distance(c.blue2.position[0], c.blue2.position[1], c.ball[0],c.ball[1]))  # distance robot green 1 et la balle


        def position_robots_adversaire():
            xb1 = c.green1.position[0]
            yb1 = c.green1.position[1]
            xb2 = c.green2.position[0]
            yb2 = c.green2.position[1]
            return xb1, yb1, xb2, yb2


        def distances_balle_adversaire(xb1, yb1, xb2, yb2):
            db1 = math.sqrt(((xb1 - c.ball[0]) ** 2) + ((yb1 - c.ball[1]) ** 2))
            db2 = math.sqrt(((xb2 - c.ball[0]) ** 2) + ((yb2 - c.ball[1]) ** 2))
            return db1,db2

        def attaquant_adverse(db1,db2):
            coor = position_robots_adversaire()
            d = distances_balle_adversaire(coor[0],coor[1],coor[2],coor[3])
            if db1 > db2:
                xr = xb2
                yr = yb2
            if db1 <= db2:
                xr = xb1
                yr = yb1
            return xr,yr


        def y_gardien(db1,db2):
            xr,yr=attaquant_adverse(db1,db2)
            x = []
            y = []
            x.append(c.ball[0])
            x.append(xr)
            y.append(c.ball[1])
            y.append(yr)
            a, b = np.polyfit(x, y, 1)[0], np.polyfit(x, y, 1)[1]
            y_goal = a * 0.8 + b
            return y_goal

        def gardien(db1,db2):
            y_goal=y_gardien(db1, db2)
            c.blue2.goto(c.blue2.position[0], y_goal)

        while True:
            try:
                xb1, yb1, xb2, yb2 = position_robots_adversaire()
                db1,db2 = distances_balle_adversaire(xb1, yb1, xb2, yb2)
                gardien(db1, db2)
                y_Axe = y_Attack_a_gauche(y1)
                cos = distance2(y1)
                while d >= 0.11:  # si d <0.11 le robot est a distance pour tirer
                    positionnement1(y1,cos)
                    d=distance(c.blue1.position[0],c.blue1.position[1],c.ball[0],c.ball[1]) #actualiser "d"
                kick1(t_ref)
                t_ref = time.time()  # créer un timer de 1 sec entre chaque kick
                recule(y1,cos)
                #sortie_de_terrain()
            except BaseException as t:
                        print("Il y a une erreur: ")
                        print(t)
                        print(traceback.format_exc())
                        pass
        

        def stop():
            c.blue1.goto((c.blue1.position[0], c.blue1.position[1], math.pi), wait = False) # stop le robot a sa position actuelle.

        stop()


