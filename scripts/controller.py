#!/usr/bin/env python3
import random 
import rospy
from Task1.srv import Service2, Service2Response ,Service3, Service3Response
from std_msgs.msg import Int32MultiArray


def car1(msg):
    x=msg.data[0]
    y=msg.data[1]
    s=msg.data[2]
    
def car2(msg):
    x=msg.data[0]
    y=msg.data[1]
    s=msg.data[2]

def car3(msg):
    x=msg.data[0]
    y=msg.data[1]
    s=msg.data[2]


def interrrupt(req):

    if (sub1.x==req.xnu and sub1.y==req.ynu) or (sub2.x==req.xnu and sub2.y==req.ynu) or (sub3.x==req.xnu and sub3.y==req.ynu) :
        aprv=0
    else:
        aprv=1
        
    response=Service2Response(aprv)
    return response


def move(req):
    
          rnds1=0
          rnds2=0
          rnds3=0
          rej=[]
          if sub1.x==req.xn and sub1.y==req.yn  : #if there is a car in the targt cell
              aprv=0 #reject movement
              rej[req.CID-1]=1 # important for next conditions not here
              if sub1.s==1 or rej[0]==1: #if the obstecale is statinoary or blocked // IF NOT just wait
               rnds1=1 # move it with random move(this obstacle is gonna be only who are doing requests)
               rnds2=-1
               rnds3=-1
               rej[0]=0
              


          elif sub2.x==req.xn and sub2.y==req.yn  :
              aprv=0
              rej[req.CID-1]=1
              if sub2.s==1 or rej[1]==1:
               rnds2=1
               rnds1=-1
               rnds3=-1
               rej[1]=0
              



          elif sub3.x==req.xn and sub3.y==req.yn  :
              aprv=0
              rej[req.CID-1]=1
              if sub3.s==1 or rej[2]==1:
               rnds3=1
               rnds2=-1
               rnds1=-1
               rej[2]=0
              


        
          else:
           aprv=1

          response=Service2Response(aprv,rnds1,rnds2,rnds3)
         
          return response


    

if __name__=='__main__':
    
    rospy.init_node("control")
    sub1= rospy.Subscriber('/car1',Int32MultiArray,car1)

    sub2=rospy.Subscriber('/car2',Int32MultiArray,car2)

    sub3=rospy.Subscriber('/car3',Int32MultiArray,car3)

    rospy.Service('control',Service2,move)

    rospy.Service('int',Service3,interrrupt)

    

    rospy.spin()

