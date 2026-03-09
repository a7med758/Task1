#!/usr/bin/env python3
import random 
import itertools
import rospy
from Task1.srv import Service1, Service1Response

all=list(itertools.product(range(0,9),repeat=2))

unipu=random.sample(all,5)



unipux,unipuy=zip(*(unipu))


unido=random.sample(all,5)

unidox,unidoy=zip(*(unido))

 # generate tasks

class TASK:

    def __init__(self, ID, PU, DO, x, y):
        self.ID = ID
        self.PU = PU
        self.DO = DO
        self.x = x
        self.y = y


TS = []  # List to store the TASK objects
IDs = [0,1, 2, 3, 4, 5, 6, 7, 8, 9]

IDpu = [1, 3,  5,  7,  9]

IDdo = [ 0,2,  4, 6,  8]

PU = 1  # Initial value for PU
DO = 0  # Initial value for DO

k=0
for ID in IDpu:
    
    x=unipux[k]
    y=unipuy[k]
    TS.append(TASK(ID, PU, DO, x, y))  # Create a TASK object and add it to TS
    k=k+1

PU = 0  
DO = 1 

k=0
for ID in IDdo:
    
    x=unidox[k]
    y=unidoy[k]
    TS.append(TASK(ID, PU, DO, x, y))  # Create a TASK object and add it to TS
    k=k+1




def handle_calac(req):
    
   if not IDs:
     response=Service1Response(0, 0, 0, -1, -1) # no more tasks
   else:  
    if req.id == -1:
        # If this is the first task, return a random task from TS and remove it
        i = random.choice(IDpu)  
        
        

    else:
        #######// add log info for completed later //#######
       
        if TS[req.id].PU == 1 :
           
            for i in IDdo:   # Pick up location not equal the drop off
                if (TS[req.id].x != TS[i].x and TS[req.id].y != TS[i].y):
                    break
                
                IDdo.remove(i)


        else:
           
            for i in IDpu:   
                if (TS[req.id].x != TS[i].x and TS[req.id].y != TS[i].y):
                    break
                
                IDpu.remove(i)
        
        
        
        
        
    task = TS[i]
    IDs.remove(i)  # Remove the task
    # Once a valid task is found, remove it and return the response
    response=Service1Response(task.PU, task.DO, task.ID, task.x, task.y)
         
    return response
    


def main():
    rospy.init_node("task")
    rospy.Service('task',Service1, handle_calac)

    rospy.spin()


if __name__=='__main__':
    
    main()
