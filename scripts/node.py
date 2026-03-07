#!/usr/bin/env python3
import random 
import rospy
from Task1.srv import Service1, Service1Response

if __name__=='__main__':
    rospy.init_node("task")
    
 # generate tasks

class TASK:

    def __init__(self, ID, PU, DO, x, y):
        self.ID = ID
        self.PU = PU
        self.DO = DO
        self.x = x
        self.y = y


TS = []  # List to store the TASK objects
IDs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

PU = 1  # Initial value for PU
DO = 0  # Initial value for DO

# Variables to store x and y values from the if block for comparison
prev_x, prev_y = None, None

for ID in IDs:
    if PU == 1:  # Check if PU is 1
        x = random.randint(0, 8)  # Random integer between 0 and 8
        y = random.randint(0, 8)  # Random integer between 0 and 8
    
        TS.append(TASK(ID, PU, DO, x, y))  # Create a TASK object and add it to TS
        PU = 0  # Switch PU to 0
        DO = 1  # Switch DO to 1
        
        # Store the random x and y values for later comparison
        prev_x, prev_y = x, y

    else:  # If PU is 0
        # Ensure that the random values for x and y are not the same as the ones in the if block
        while True:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if x != prev_x or y != prev_y:  # Ensure x and y are not equal to the previous ones
                break
        
        TS.append(TASK(ID, PU, DO, x, y))  # Create a TASK object and add it to TS
        DO = 0  # Switch DO to 0
        PU = 1  # Switch PU to 1



def handle_calac(req):
    l = len(TS)
    i = random.choice(TS)  # Ensure valid index range (0 to l-1)

    if req.id == 0:
        # If request ID is 0, return a random task from TS and remove it
        response=Service1Response(task.PU, task.DO, task.ID, task.x, task.y)
        task = TS[i]
        TS.remove(task)  # Remove task 
        return response

    else:
        # Loop to find a valid task with different PU or DO
        while TS[req.id].PU == TS[i].PU or TS[req.id].DO == TS[i].DO:
            i = random.choice(TS)  # Pick a new random index

        # Once a valid task is found, remove it and return the response
        task = TS[i]
        response=Service1Response(task.PU, task.DO, task.ID, task.x, task.y)
        TS.remove(task)  # Remove the task 
        return response
    

rospy.Service('task',Service1, handle_calac)

rospy.spin()