import os
from dynamixel_sdk import *
import time
import json
import numpy as np

# Control table address
ADDR_PRO_TORQUE_ENABLE = 24  # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION = 30
ADDR_PRO_PRESENT_POSITION = 37
ADDR_PRO_OPERATING_MODE = 11
ADDR_PRO_MOVING_SPEED = 32

# Protocol version
PROTOCOL_VERSION = 2.0  # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID1 = 1  # Dynamixel ID : 1
DXL_ID2 = 2
DXL_ID3 = 3
DXL_ID4 = 4
DXL_ID5 = 5
BAUDRATE = 1000000  # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/tty.usbserial-FT2H2MO1'  # Check which port is being used on your controller
# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE = 0  # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE = 1000  # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20  # Dynamixel moving status threshold


FLOWERPOT = 1
PAPERTOWEL = 2
PIGGYBANK = 3

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

for motor_id in range(1,14):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)

    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, motor_id,
                                                                                   ADDR_PRO_PRESENT_POSITION)
    print(dxl_present_position)

    packetHandler.write2ByteTxRx(portHandler, motor_id, ADDR_PRO_MOVING_SPEED,120)
packetHandler.write2ByteTxRx(portHandler, 13, ADDR_PRO_MOVING_SPEED, 200)

# flower pot
motor_value_1 = np.array([[832, 516, 512, 494],
                            [832, 516, 512, 225],
                            [832, 516, 350, 225],
                            [256, 751, 601, 225],
                            [256, 520, 601, 225],
                            [490, 534, 376, 641],
                            [490, 750, 376, 641],
                            [490, 570, 376, 175],
                            [832, 570, 520, 175],
                            [832, 470, 520, 500]])
# paper towel holder
motor_value_2 = np.array([[486, 513, 529, 514],
                            [440, 513, 529, 740],
                            [440, 513, 830, 740],
                            [440, 750, 830, 740],
                            [440, 750, 600, 600],
                            [440, 750, 600, 740],
                            [440, 750, 830, 740],
                            [440, 600, 830, 740],
                            [440, 600, 530, 530],
                            [440, 530, 530, 530],
                            [480, 530, 530, 530]])

# piggy bank
motor_value_3 = np.array([[476, 550, 498, 450, 846],
                            [476, 550, 498, 256, 846],
                            [476, 550, 242, 256, 846],
                            [360, 550, 242, 256, 846],
                            [360, 550, 242, 256, 200],
                            [360, 750, 430, 350, 200],
                            [360, 750, 430, 350, 846],
                            [360, 750, 430, 250, 846],
                            [360, 750, 240, 250, 846],
                            [360, 550, 240, 250, 846],
                            [476, 550, 240, 250, 846],
                            [476, 550, 500, 450, 846]])

order4 = np.array([1, 2, 3, 4])
order5 = np.array([1, 2, 3, 4, 5])

while 1:
    object_type = input("what is the object to demo: ")
    if object_type == FLOWERPOT:
        num = len(motor_value_1)
        for i in range(num):
            motor_value = motor_value_1[i]
            # id_now = 4
            order_index = 0
            # if i == 4 or i == 9: # wait for action
            #     time.sleep(6)
            while 1:
                id_now = order4[order_index]
                obj_value = int(motor_value[id_now - 1])

                packetHandler.write2ByteTxRx(portHandler, id_now, ADDR_PRO_GOAL_POSITION, obj_value)
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, id_now,
                                                                                               ADDR_PRO_PRESENT_POSITION)
                if abs(dxl_present_position - obj_value) < 50:
                    order_index += 1

                if order_index >= 4:
                    break

    elif object_type == PAPERTOWEL:
        num = len(motor_value_2)
        for i in range(num):
            motor_value = motor_value_2[i]
            # id_now = 4
            order_index = 0
            if i == 5:  # wait for action
                time.sleep(6)
            while 1:
                id_now = order4[order_index]
                obj_value = int(motor_value[id_now - 1])

                packetHandler.write2ByteTxRx(portHandler, id_now+4, ADDR_PRO_GOAL_POSITION, obj_value)
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, id_now+4,
                                                                                               ADDR_PRO_PRESENT_POSITION)
                if abs(dxl_present_position - obj_value) < 50:
                    order_index += 1

                if order_index >= 4:
                    break

    elif object_type == PIGGYBANK:
        num = len(motor_value_3)
        for i in range(num):
            motor_value = motor_value_3[i]
            # id_now = 4
            order_index = 0
            # if i == 4 or i == 9:  # wait for action
            #     time.sleep(6)
            while 1:
                id_now = order5[order_index]
                obj_value = int(motor_value[id_now - 1])

                packetHandler.write2ByteTxRx(portHandler, id_now+8, ADDR_PRO_GOAL_POSITION, obj_value)
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, id_now+8,
                                                                                               ADDR_PRO_PRESENT_POSITION)
                if abs(dxl_present_position - obj_value) < 50:
                    order_index += 1

                if order_index >= 5:
                    break