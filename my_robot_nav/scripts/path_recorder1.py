#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped

path_pub = rospy.Publisher('/recorded_path', Path, queue_size=10)
path_data = Path()

def odom_cb(data):
    global path_data
    path_data.header.frame_id = "map"
    pose = PoseStamped()
    pose.header = data.header
    pose.pose = data.pose.pose
    path_data.poses.append(pose)
    path_pub.publish(path_data)

if __name__ == '__main__':
    rospy.init_node('recorder')
    rospy.Subscriber('/odom', Odometry, odom_cb)
    rospy.spin()
