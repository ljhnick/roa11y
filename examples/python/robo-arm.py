import os
from dynamixel_sdk import *
import time
import json
import numpy as np
import math

import httplib2

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

    PROFILE_VELOCITY = 30

    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Robotic arm dimensions
    Link1 = 150
    Link2 = 200


    def torque_enable_all(self):
        for i in range(0, self.ID_all.__len__()):
            self.packetHandler.write1ByteTxRx(self.portHandler, self.ID_all[i], self._TORQUE_ENABLE, self.TORQUE_ENABLE)

    def torque_disable_all(self):
        for i in range(0, self.ID_all.__len__()):
            self.packetHandler.write1ByteTxRx(self.portHandler, self.ID_all[i], self._TORQUE_ENABLE, self.TORQUE_DISABLE)

    def set_profile_velocity(self):
        for i in range(0, self.ID_all.__len__()):
            self.packetHandler.write4ByteTxRx(self.portHandler, self.ID_all[i], self._PROFILE_VELOCITY, self.PROFILE_VELOCITY)
            if i >= 3:
                self.packetHandler.write4ByteTxRx(self.portHandler, self.ID_all[i], self._PROFILE_VELOCITY,
                                                  50)

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

        theta4_deg = -(theta2_deg + theta3_deg) + tar_ori[0] + 10
        theta5_deg = -theta1_deg + tar_ori[1]
        theta6_deg = tar_ori[2]

        theta4_deg = min(theta4_deg, 35)

        tar_q = np.array([theta1_deg, theta2_deg, theta3_deg, theta4_deg, theta5_deg, theta6_deg])

        self.set_pos_all(tar_q)
        return tar_q

    def sleep(self):
        sleep_q = np.array([0, 85, -85, -85, 0, 0])
        self.set_pos_all(sleep_q)

    def wakeup(self):
        wake_q = np.array([0, 60, -30, 0, 0, 90])
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
        self.wakeup()


robotic_arm = RoboArm()

print(1)

http = httplib2.Http()
url = "http://192.168.86.34/test"
headers = {"Content-Type": "application/json; charset=UTF-8"}
data1 = {"id":"5", "speed":"1023"}
data2 = {"id":"5", "speed":"0"}
response, content = http.request(url, "POST", headers=headers, body=json.dumps(data2))

robotic_arm.sleep()
robotic_arm.torque_disable_all()