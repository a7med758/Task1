#!/usr/bin/env python3
import random 
import rospy
from Task1.srv import Service1, Service1Response



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



for ID in IDs:
    if PU == 1:  # Check if PU is 1
       
        x = random.randint(0, 8)
        y = random.randint(0, 8)
            
    
        TS.append(TASK(ID, PU, DO, x, y))  # Create a TASK object and add it to TS
        PU = 0  # Switch PU to 0
        DO = 1  # Switch DO to 1
        
        

    else:  # If PU is 0
        # Ensure that the random values for x and y are not the same as the ones in the if block
        
        x = random.randint(0, 8)
        y = random.randint(0, 8)
            
        
        TS.append(TASK(ID, PU, DO, x, y))  # Create a TASK object and add it to TS
        DO = 0  # Switch DO to 0
        PU = 1  # Switch PU to 1



def handle_calac(req):
    
   if not IDs:
     response=Service1Response(0, 0, 0, -1, -1) # no more tasks
   else:  
    if req.id == -1:
        # If this is the first task, return a random task from TS and remove it
        i = random.choice(IDs)  
        
        

    else:
        #######// add log info for completed later //#######
        # Loop to find a valid task with different PU or DO
        if TS[req.id].PU == 1 :
           
            for i in IDdo:   # Pick a new index
                if (TS[req.id].x != TS[i].x and TS[req.id].y != TS[i].y):
                    break
                elif i==max(IDdo):
                    while True:
                        x = random.randint(0, 8)
                        y = random.randint(0, 8)
                        if x != TS[req.id].x and y != TS[req.id].y:  # Ensure x and y are not equal to the previous ones
                            break
                    TS[i]=TASK(i, 0, 1, x, y)
                IDdo.remove(i)


        else:
           
            for i in IDpu:   # Pick a new  index with diffrent location
                if (TS[req.id].x != TS[i].x and TS[req.id].y != TS[i].y):
                    break
                elif i==max(IDpu): # all locations are invalid so generate new one and replace it 
                    while True:
                        x = random.randint(0, 8)
                        y = random.randint(0, 8)
                        if x != TS[req.id].x and y != TS[req.id].y:  
                            break
                    TS[i]=TASK(i, 0, 1, x, y)
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
