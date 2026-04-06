#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String, Float32

class DepthNode:
    def __init__(self):
        # 1. تعريف النود
        rospy.init_node('depth_node', anonymous=False)
        
        # 2. الناشرين لنود 4 و 8
        self.depth_info_pub = rospy.Publisher('/depth_info', String, queue_size=10)
        self.monitor_status_pub = rospy.Publisher('/depth_status', String, queue_size=10)
        
        # 3. الاشتراك في العرض المبعوث من نود 2
        rospy.Subscriber('/object_width', Float32, self.width_callback)

    def width_callback(self, msg):
        box_width = msg.data
        
        # حساب المسافة بناءً على "العرض البؤري" (Focal Length simulation)
        # المعادلة: Distance = (FocalLength * RealWidth) / PixelWidth
        # هنثبت الثابت ده عند 350.0 (قابلة للمعايرة)
        focal_constant = 350.0 
        
        if box_width > 10:
            estimated_distance = round(focal_constant / box_width, 2)
            
            # تحديد الحالة بناءً على الرقم
            if estimated_distance < 1.0:
                zone = "CRITICAL ZONE"
            elif estimated_distance < 2.5:
                zone = "WARNING ZONE"
            else:
                zone = "SAFE ZONE"
            
            full_msg = f"Dist: {estimated_distance}m ({zone})"
        else:
            # لو مفيش جسم واضح، نعتبر المسافة بعيدة جداً
            full_msg = "Dist: > 5.0m (Idle)"

        # 4. النشر لنود التحليل (نود 4) وللجدول (نود 8)
        self.depth_info_pub.publish(full_msg)
        self.monitor_status_pub.publish(full_msg)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node = DepthNode()
    node.run()
