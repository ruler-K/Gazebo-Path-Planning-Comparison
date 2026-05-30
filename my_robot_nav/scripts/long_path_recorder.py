#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped

class ContinuousPath:
    def __init__(self):
        rospy.init_node('continuous_path_recorder')
        # 订阅里程计获取实时坐标
        self.sub = rospy.Subscriber('/odom', Odometry, self.odom_cb)
        # 发布一个专门的连续轨迹话题
        self.pub = rospy.Publisher('/stable_trajectory', Path, queue_size=10)
        
        self.path = Path()
        self.path.header.frame_id = "map" # 核心：绑定在地图坐标系，保证线不随车动

    def odom_cb(self, data):
        # 创建新点
        current_pose = PoseStamped()
        current_pose.header = data.header
        current_pose.header.frame_id = "map"
        current_pose.pose = data.pose.pose
        
        # 将当前点追加到列表末尾，从不删除旧点
        self.path.poses.append(current_pose)
        self.path.header.stamp = rospy.Time.now()
        
        # 发布完整路径
        self.pub.publish(self.path)

if __name__ == '__main__':
    try:
        ContinuousPath()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
