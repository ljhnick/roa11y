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
DXL_ID6 = 6
DXL_ID7 = 7
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

for motor_id in range(1,8):
    packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, motor_id,
                                                                                   ADDR_PRO_PRESENT_POSITION)
    print(dxl_present_position)
    packetHandler.write2ByteTxRx(portHandler, motor_id, ADDR_PRO_MOVING_SPEED, 120)

packetHandler.write2ByteTxRx(portHandler, 7, ADDR_PRO_MOVING_SPEED, 0)

print(1)