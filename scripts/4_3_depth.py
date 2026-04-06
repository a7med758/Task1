#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String, Float32

class DepthNode:
    def __init__(self):
        # 1. Initialize the ROS node
        rospy.init_node('depth_node', anonymous=False)
        
        # 2. Publishers for Node 4 (analysis) and Node 8 (monitoring/dashboard)
        self.depth_info_pub = rospy.Publisher('/depth_info', String, queue_size=10)
        self.monitor_status_pub = rospy.Publisher('/depth_status', String, queue_size=10)
        
        # 3. Subscribe to object width topic coming from Node 2
        self.width_sub = rospy.Subscriber('/object_width', Float32, self.width_callback)

    def width_callback(self, msg):
        # Extract detected bounding box width (in pixels)
        box_width = msg.data
        
        # Estimate distance using a simplified focal length formula:
        # Distance = (FocalLength * RealWidth) / PixelWidth
        # Here we simulate (FocalLength * RealWidth) as a constant
        focal_constant = 350.0  # Tunable calibration constant
        
        if box_width > 10:
            # Calculate estimated distance (in meters)
            estimated_distance = round(focal_constant / box_width, 2)
            
            # Determine safety zone based on distance
            if estimated_distance < 1.0:
                zone = "CRITICAL ZONE"
            elif estimated_distance < 2.5:
                zone = "WARNING ZONE"
            else:
                zone = "SAFE ZONE"
            
            # Format output message
            full_msg = f"Dist: {estimated_distance}m ({zone})"
        else:
            # If no valid object is detected, assume very far distance
            full_msg = "Dist: > 5.0m (Idle)"

        # 4. Publish results to both analysis node and monitoring/dashboard node
        self.depth_info_pub.publish(full_msg)
        self.monitor_status_pub.publish(full_msg)

    def run(self):
        # Keep the node running and listening for incoming messages
        rospy.spin()

if __name__ == '__main__':
    node = DepthNode()
    node.run()
