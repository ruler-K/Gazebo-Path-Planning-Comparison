#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped

class PathRecorder:
    def __init__(self):
        rospy.init_node('path_recorder_node')
        # 订阅里程计，获取小车实时位置
        self.sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        # 发布轨迹线话题
        self.path_pub = rospy.Publisher('/recorded_trajectory', Path, queue_size=10)
        
        self.trajectory = Path()
        self.trajectory.header.frame_id = "map" # 绑定在地图坐标系上

    def odom_callback(self, msg):
        # 创建一个位姿点
        current_pose = PoseStamped()
        current_pose.header = msg.header
        current_pose.header.frame_id = "map"
        current_pose.pose = msg.pose.pose
        
        # 将当前点加入轨迹列表
        self.trajectory.poses.append(current_pose)
        self.trajectory.header.stamp = rospy.Time.now()
        
        # 发布完整轨迹
        self.path_pub.publish(self.trajectory)

if __name__ == '__main__':
    recorder = PathRecorder()
    rospy.spin()
