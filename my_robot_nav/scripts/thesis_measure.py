#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
import math
import time

class ThesisMeasurer:
    def __init__(self):
        self.last_time = None
        self.sub = rospy.Subscriber('/move_base/GlobalPlanner/plan', Path, self.callback)
        print("--- 实验数据采集节点已启动 ---")

    def callback(self, data):
        # 1. 计算路径长度
        points = data.poses
        dist = 0.0
        for i in range(len(points) - 1):
            p1 = points[i].pose.position
            p2 = points[i+1].pose.position
            dist += math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
        
        # 2. 计算耗时
        current_time = time.time()
        if self.last_time is not None:
            duration = current_time - self.last_time
            print(f"--- 实时数据 ---")
            print(f"路径总长度: {dist:.4f} 米")
            print(f"规划周期 (T): {duration:.4f} 秒")
            print(f"规划耗时 (ms): {duration*1000:.2f} 毫秒")
            print(f"实时频率 (f): {1.0/duration:.2f} Hz")
            print(f"----------------\n")
        
        self.last_time = current_time

if __name__ == '__main__':
    rospy.init_node('thesis_measure_node')
    measurer = ThesisMeasurer()
    rospy.spin()
