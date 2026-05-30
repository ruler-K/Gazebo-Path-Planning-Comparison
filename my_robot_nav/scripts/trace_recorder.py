#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped

class TraceRecorder:
    def __init__(self):
        rospy.init_node('trace_recorder_node')
        # 订阅里程计
        self.sub = rospy.Subscriber('/odom', Odometry, self.odom_cb)
        # 发布一个自定义轨迹话题
        self.pub = rospy.Publisher('/final_trajectory', Path, queue_size=1)
        
        self.path = Path()
        self.path.header.frame_id = "map" # 必须绑定在 map 坐标系

    def odom_cb(self, data):
        # 将当前位置存入路径点列表
        node = PoseStamped()
        node.header = data.header
        node.header.frame_id = "map"
        node.pose = data.pose.pose
        
        # 只有当位置发生变化时才记录，防止数据量过大
        self.path.poses.append(node)
        self.path.header.stamp = rospy.Time.now()
        # 持续发布完整路径
        self.pub.publish(self.path)

if __name__ == '__main__':
    TraceRecorder()
    rospy.spin()
