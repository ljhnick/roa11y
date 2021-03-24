import os
from dynamixel_sdk import *
import time
import json
import numpy as np
import math

import httplib2

from interaction_ui import Gripper

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()

class RoboArm:
    # Protocol version
    PROTOCOL_VERSION = 2.0  # See which protocol version is used in the Dynamixel

    # Control table
    _TORQUE_ENABLE = 64
    _GOAL_POSITION = 116
    _PRESENT_POSITION = 132
    _PROFILE_VELOCITY = 112

    # Dynamixel ID
    ID1 = 2
    ID2 = 6
    ID3 = 9
    ID4 = 5
    ID5 = 3
    ID6 = 1
    ID_all = [ID1, ID2, ID3, ID4, ID5, ID6]

    BAUDRATE = 1000000  # Dynamixel default baudrate : 57600
    DEVICENAME = '/dev/tty.usbserial-FT2H2MO1'  # Check which port is being used on your controller

    TORQUE_ENABLE = 1  # Value for enabling the torque
    TORQUE_DISABLE = 0  # Value for disabling the torque

    PROFILE_VELOCITY = 20

    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Robotic arm dimensions
    Link1 = 160
    Link2 = 180


    def torque_enable_all(self):
        for i in range(0, self.ID_all.__len__()):
            self.packetHandler.write1ByteTxRx(self.portHandler, self.ID_all[i], self._TORQUE_ENABLE, self.TORQUE_ENABLE)

    def torque_disable_all(self):
        for i in range(0, self.ID_all.__len__()):
            self.packetHandler.write1ByteTxRx(self.portHandler, self.ID_all[i], self._TORQUE_ENABLE, self.TORQUE_DISABLE)

    def set_profile_velocity(self):
        for i in range(0, self.ID_all.__len__()):
            self.packetHandler.write4ByteTxRx(self.portHandler, self.ID_all[i], self._PROFILE_VELOCITY, self.PROFILE_VELOCITY)
            # if i >= 3:
            #     self.packetHandler.write4ByteTxRx(self.portHandler, self.ID_all[i], self._PROFILE_VELOCITY,
            #                                       50)
        # self.packetHandler.write4ByteTxRx(self.portHandler, self.ID_all[1], self._PROFILE_VELOCITY,
        #                                   10)

    def read_position_pulse(self, index):
        pos, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.ID_all[index], self._PRESENT_POSITION)
        # print('The motor ' + str(ID) + ' value is: ' + str(pos))
        return pos

    def read_position_deg(self, index):
        pos, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.ID_all[index], self._PRESENT_POSITION)
        # print('The motor ' + str(ID) + ' value is: ' + str(pos))
        if index == 2:
            diff = pos - 1024
        else:
            diff = pos - 2048
        deg = 0 + int(diff*0.088)
        return deg

    def read_pos_all(self):
        position = np.zeros(6)
        for i in range(6):
            pos = self.read_position_deg(i)
            position[i] = pos

        return position

    def set_position_pulse(self, index, pos):
        self.packetHandler.write4ByteTxRx(self.portHandler, self.ID_all[index], self._GOAL_POSITION, pos)

    def set_position_deg(self, index, deg):
        diff = int((deg - 0)/0.088)

        if index == 0:
            pulse = diff + 2048
        elif index == 1:
            pulse = diff + 2048
        elif index == 2:
            pulse = diff + 1024
        elif index == 3:
            pulse = diff + 2048
        elif index == 4:
            pulse = diff + 2048
        elif index == 5:
            pulse = diff + 2048

        self.set_position_pulse(index, pulse)

    def set_pos_all(self, tar_q):
        for i in range(0, len(tar_q)):
            self.set_position_deg(i, tar_q[i])

        flag = False
        while 1:
            for i in range(0, len(tar_q)):
                deg = self.read_position_deg(i)
                if abs(deg - tar_q[i]) >= 10:
                    flag = False
                    break
                else:
                    flag = True

            if flag:
                break

    def ikine(self, tar_pos):
        x = tar_pos[0]
        y = tar_pos[1]
        z = tar_pos[2]

        a = math.sqrt(x * x + y * y)
        b = z

        theta1 = math.atan2(y, x)
        theta3 = np.arcsin(-(self.Link1 ** 2 + self.Link2 ** 2 - a ** 2 - b ** 2) / (2 * self.Link1 * self.Link2))

        c = self.Link1 + self.Link2 * np.sin(theta3)
        d = self.Link2 * np.cos(theta3)
        theta_cd = np.arctan(c / d)
        theta2 = np.arcsin(b / math.sqrt(d ** 2 + c ** 2)) - theta_cd

        theta1_deg = theta1 / math.pi * 180
        theta2_deg = theta2 / math.pi * 180
        theta3_deg = theta3 / math.pi * 180

        theta = np.array([theta1_deg, theta2_deg, theta3_deg])

        return theta

    def move_to_target_point(self, tar_pos, tar_ori):
        x = tar_pos[0]
        y = tar_pos[1]
        z = tar_pos[2]

        a = math.sqrt(x*x+y*y)
        b = z

        theta1 = math.atan2(y, x)
        theta3 = np.arcsin(-(self.Link1**2+self.Link2**2-a**2-b**2)/(2*self.Link1*self.Link2))

        c = self.Link1+self.Link2*np.sin(theta3)
        d = self.Link2*np.cos(theta3)
        theta_cd = np.arctan(c/d)
        theta2 = np.arcsin(b/math.sqrt(d**2+c**2))-theta_cd

        theta1_deg = theta1/math.pi*180
        theta2_deg = theta2/math.pi*180
        theta3_deg = theta3/math.pi*180

        # theta4 = -math.atan2((z-(self.Link1+30)*np.cos(theta2)), a+self.Link1*np.sin(theta2))
        theta4_off = 10/180*math.pi
        theta4 = -(theta2 + theta3) + theta4_off + tar_ori[0]/180*math.pi

        # if condition:
        #     theta4 = theta4 - math.pi/2

        theta5 = -theta1
        theta6 = tar_ori[2]/180*math.pi



        # theta3 = theta3 - math.pi/2
        # theta2 = theta2 + math.pi/2
        #
        # R0_1 = np.array([[np.cos(theta1), -np.sin(theta1), 0], [np.sin(theta1), np.cos(theta1), 0], [0, 0, 1]])
        # R1_2 = np.array([[np.cos(theta2), -np.sin(theta2), 0], [0, 0, -1], [np.sin(theta2), np.cos(theta2), 0]])
        # R2_3 = np.array([[np.cos(theta3), -np.sin(theta3), 0], [np.sin(theta3), np.cos(theta3), 0], [0, 0, 1]])
        #
        # R0_3 = np.matmul(np.matmul(R0_1, R1_2), R2_3)
        #
        # R3_6 = np.linalg.inv(R0_3) * tar_ori
        # theta5 = np.arccos(-R3_6[2][2])
        # theta6 = np.arcsin(R3_6[2][1]/np.sin(theta5))
        # a_r = np.sin(theta6)
        # b_r = np.cos(theta5)*np.cos(theta6)
        # theta4 = np.arcsin(R3_6[0][0]/math.sqrt(a_r**2+b_r**2))-np.arctan(b_r/a_r)
        # theta5 = theta5 - math.pi/2
        #
        theta4_deg = theta4 / math.pi * 180
        theta5_deg = theta5 / math.pi * 180
        theta6_deg = theta6 / math.pi * 180


        # theta4_deg = -(theta2_deg + theta3_deg) + tar_ori[0] + 10
        # theta5_deg = -theta1_deg + tar_ori[1]
        # theta6_deg = tar_ori[2]
        #
        # theta4_deg = min(theta4_deg, 30)

        tar_q = np.array([theta1_deg, theta2_deg, theta3_deg, theta4_deg, theta5_deg, theta6_deg])

        self.set_pos_all(tar_q)
        return tar_q

    def move_to_target_point_smooth(self, tar_pos, tar_ori):

        # smooth_level = 10
        #
        # current_q = self.read_pos_all()
        # theta1_rad = current_q[0] / 180 * math.pi
        # theta2_rad = current_q[1] / 180 * math.pi
        # theta3_rad = current_q[2] / 180 * math.pi
        #
        # cur_d = -self.Link1*np.sin(theta2_rad) + self.Link2*np.cos(theta2_rad+theta3_rad)
        # cur_z = self.Link1*np.cos(theta2_rad) + self.Link2*np.sin(theta2_rad+theta3_rad)
        # cur_x = cur_d * np.cos(theta1_rad)
        # cur_y = cur_d * np.sin(theta1_rad)
        #
        # cur_pos = np.array([cur_x, cur_y, cur_z])
        #
        # delta_d = (tar_pos - cur_pos) / smooth_level
        #
        # for i in range(smooth_level):
        #     tar_pos_mid = cur_pos + delta_d*i
        #     self.move_to_target_point(tar_pos_mid, tar_ori)

        x = tar_pos[0]
        y = tar_pos[1]
        z = tar_pos[2]

        a = math.sqrt(x * x + y * y)
        b = z

        tar_pos_q = self.ikine(tar_pos)

        current_q = self.read_pos_all()
        theta1_rad = current_q[0] / 180 * math.pi
        theta2_rad = current_q[1] / 180 * math.pi
        theta3_rad = current_q[2] / 180 * math.pi

        # theta4_rad = -math.atan2((z-(self.Link1+30)*np.cos(theta2_rad)), a+self.Link1*np.sin(theta2_rad))
        theta4_rad = -(theta2_rad + theta3_rad)
        theta4_deg = theta4_rad / math.pi * 180 + 10

        current_q[3] = theta4_deg
        self.set_pos_all(current_q)

        time.sleep(2)
        while 1:
            current_q = self.read_pos_all()
            theta1_rad = current_q[0] / 180 * math.pi
            theta2_rad = current_q[1] / 180 * math.pi
            theta3_rad = current_q[2] / 180 * math.pi

            # theta4_rad = -math.atan2((z - (self.Link1 + 30) * np.cos(theta2_rad)), a + self.Link1 * np.sin(theta2_rad))
            theta4_rad = -(theta2_rad + theta3_rad)
            theta4_deg = theta4_rad / math.pi * 180 + 10

            tar_q_mid = np.r_[tar_pos_q, np.array([theta4_deg, 0, 0])]
            self.set_pos_all(tar_q_mid)

            cur_d = -self.Link1*np.sin(theta2_rad) + self.Link2*np.cos(theta2_rad+theta3_rad)
            cur_z = self.Link1*np.cos(theta2_rad) + self.Link2*np.sin(theta2_rad+theta3_rad)
            cur_x = cur_d * np.cos(theta1_rad)
            cur_y = cur_d * np.sin(theta1_rad)

            cur_pos = np.array([cur_x, cur_y, cur_z])
            dist = np.linalg.norm(tar_pos - cur_pos)
            if dist <= 30:
                break

    def test(self):
        test_q = np.array([0, 116, -86, -36, -95, 0])
        self.set_pos_all(test_q)

    def sleep(self):
        sleep_q = np.array([0, 116, -86, 90, 0, 0])
        self.wakeup()
        self.set_pos_all(sleep_q)

    def wakeup(self):
        wake_q = np.array([0, 13, -77, 53, 0, 0])
        self.set_pos_all(wake_q)

    def __init__(self):
        self.portHandler.openPort()
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()
        self.torque_enable_all()
        self.set_profile_velocity()
        # self.wakeup()
        time.sleep(2)

# class Gripper:
#
#     def detach(self):
#         detach_addr = "/detach"
#         url = self.url + detach_addr
#         response, content = self.http.request(url, "GET")
#         return response
#
#     def actuate(self, flag=None):
#         actuate_addr = "/actuate"
#         url = self.url + actuate_addr
#
#         if flag == 1:
#             data = {"id":"5", "speed":"1023"}
#         elif flag == 2:
#             data = {"id": "5", "speed": "2047"}
#         else:
#             data = {"id":"5", "speed":"0"}
#
#         response, content = self.http.request(url, "POST", headers=self.headers, body=json.dumps(data))
#
#         return response
#
#     def __init__(self):
#         self.http = httplib2.Http()
#         self.url = "http://192.168.86.22"
#         self.headers = {"Content-Type": "application/json; charset=UTF-8"}


# initialize robotic arm
robotic_arm = RoboArm()

# tar_pos = np.array([100, 0, 200])
# tar_pos = np.array([150, 0, 100])
# tar_ori = np.array([0, 0, 0])
# robotic_arm.move_to_target_point(tar_pos, tar_ori)
#
# time.sleep(2)
#
# tar_pos = np.array([150, -100, 0])
# robotic_arm.move_to_target_point(tar_pos, tar_ori)
#
# time.sleep(2)
#
# tar_pos = np.array([150, 0, 100])
# robotic_arm.move_to_target_point(tar_pos, tar_ori)
#
# time.sleep(2)

gripper = Gripper()
gripper.actuate_object()
print(1)

# http = httplib2.Http()
# url_actuate = "http://192.168.86.22/actuate"
# url_detach = "http://192.168.86.22/detach"
# url_detect = "http://192.168.86.22/detect"
# headers = {"Content-Type": "application/json; charset=UTF-8"}
# data1 = {"id":"5", "speed":"1023"}
# data2 = {"id":"5", "speed":"0"}
# response, content = http.request(url_detect, "GET")
# response, content = http.request(url_detach, "GET")
# response, content = http.request(url_actuate, "POST", headers=headers, body=json.dumps(data2))

robotic_arm.sleep()
time.sleep(2)
robotic_arm.torque_disable_all()