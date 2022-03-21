#! /usr/bin/env python
from turtle import goto
import rospy
from competion_code.msg import *
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import tf

point_0=[0.2,1.7,0]
point_1=[0.6,3.3,3.5]
point_2=[0.3,2.8,0]
point_3=[2.0,2.7,0]
point_4=[2.1,0.2,3.5]
point_5=[2.5,-0.8,0]
point_6=[1.1,1.8,0]

points = [point_1,point_2,point_3,point_4,point_5]
class move_system_server:
    def __init__(self):
        self.server = actionlib.SimpleActionServer("target_position",ActGoalAction,self.callback,False)
        self.server.start()
        rospy.loginfo("target_position action is start")

    def callback(self,goal):
        rospy.loginfo("recieved goal")
        x = goal.x
        y = goal.y
        print("x= %f,y = %f",x,y)

        
def done_cb(state,result):
    if state == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("响应结果:%d",result.result)

def active_cb():
    rospy.loginfo("服务被激活....")


def fb_cb(fb):
    rospy.loginfo("当前进度:%.2f",fb.progress_bar)

def set_goal(x,y,th):
    goal_point = MoveBaseGoal()
    goal_point.target_pose.header.frame_id="map"
    goal_point.target_pose.header.stamp=rospy.Time(0)
    goal_point.target_pose.pose.position.x=x
    goal_point.target_pose.pose.position.y=y
    qtn=tf.transformations.quaternion_from_euler(0,0,th)
    goal_point.target_pose.pose.orientation.z=qtn[2]
    goal_point.target_pose.pose.orientation.w=qtn[3]
    return goal_point
    
def go_to(x,y,th):
    goal_point=set_goal(x,y,th)
    pub_goal.send_goal(goal_point)
    pub_goal.wait_for_result()
    rospy.loginfo("have go to %f %f",x,y)
if __name__ == "__main__":
    rospy.init_node("move_system")
    pub_goal = actionlib.SimpleActionClient("move_base",MoveBaseAction)
    pub_goal.wait_for_server()
    go_to(point_0[0],point_0[1],point_0[2])
    for point in points:
        go_to(point[0],point[1],point[2])
        rospy.sleep(1)
        go_to(point_6[0],point_6[1],point_6[2])
        rospy.sleep(1)

    # server = move_system_server()
    # rospy.spin()

