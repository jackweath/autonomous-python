# NOT MY CODE, HERE FOR REFERENCE

import time
import smbus
import datetime
import math


# I2C address vary on the device
# Default are the Adafruit LSM9DS0
MAG_ADDRESS	=	0x1D
ACC_ADDRESS	=	0x1D
GYR_ADDRESS =   0x6B

#LSM9DS0 gyrometer registers
WHO_AM_I_G	=	0x0F
CTRL_REG1_G	=	0x20
CTRL_REG2_G	=	0x21
CTRL_REG3_G	=	0x22
CTRL_REG4_G	=	0x23
CTRL_REG5_G	=	0x24
REFERENCE_G	=	0x25
STATUS_REG_G	=	0x27
OUT_X_L_G	=	0x28
OUT_X_H_G	=	0x29
OUT_Y_L_G	=	0x2A
OUT_Y_H_G	=	0x2B
OUT_Z_L_G	=	0x2C
OUT_Z_H_G	=	0x2D
FIFO_CTRL_REG_G	=	0x2E
FIFO_SRC_REG_G	=	0x2F
INT1_CFG_G	=	0x30
INT1_SRC_G	=	0x31
INT1_THS_XH_G	=	0x32
INT1_THS_XL_G	=	0x33
INT1_THS_YH_G	=	0x34
INT1_THS_YL_G	=	0x35
INT1_THS_ZH_G	=	0x36
INT1_THS_ZL_G	=	0x37
INT1_DURATION_G	=	0x38

#LSM9DS0 accelerometer and magnetometer registers
OUT_TEMP_L_XM	=	0x05
OUT_TEMP_H_XM	=	0x06
STATUS_REG_M	=	0x07
OUT_X_L_M	=	0x08
OUT_X_H_M	=	0x09
OUT_Y_L_M	=	0x0A
OUT_Y_H_M	=	0x0B
OUT_Z_L_M	=	0x0C
OUT_Z_H_M	=	0x0D
WHO_AM_I_XM	=	0x0F
INT_CTRL_REG_M	=	0x12
INT_SRC_REG_M	=	0x13
INT_THS_L_M	=	0x14
INT_THS_H_M	=	0x15
OFFSET_X_L_M	=	0x16
OFFSET_X_H_M	=	0x17
OFFSET_Y_L_M	=	0x18
OFFSET_Y_H_M	=	0x19
OFFSET_Z_L_M	=	0x1A
OFFSET_Z_H_M	=	0x1B
REFERENCE_X	=	0x1C
REFERENCE_Y	=	0x1D
REFERENCE_Z	=	0x1E
CTRL_REG0_XM	=	0x1F
CTRL_REG1_XM	=	0x20
CTRL_REG2_XM	=	0x21
CTRL_REG3_XM	=	0x22
CTRL_REG4_XM	=	0x23
CTRL_REG5_XM	=	0x24
CTRL_REG6_XM	=	0x25
CTRL_REG7_XM	=	0x26
STATUS_REG_A	=	0x27
OUT_X_L_A	=	0x28
OUT_X_H_A	=	0x29
OUT_Y_L_A	=	0x2A
OUT_Y_H_A	=	0x2B
OUT_Z_L_A	=	0x2C
OUT_Z_H_A	=	0x2D
FIFO_CTRL_REG	=	0x2E
FIFO_SRC_REG	=	0x2F
INT_GEN_1_REG	=	0x30
INT_GEN_1_SRC	=	0x31
INT_GEN_1_THS	=	0x32
INT_GEN_1_DURATION	=	0x33
INT_GEN_2_REG	=	0x34
INT_GEN_2_SRC	=	0x35
INT_GEN_2_THS	=	0x36
INT_GEN_2_DURATION	=	0x37
CLICK_CFG	=	0x38
CLICK_SRC	=	0x39
CLICK_THS	=	0x3A
TIME_LIMIT	=	0x3B
TIME_LATENCY	=	0x3C
TIME_WINDOW	=	0x3D

# Setting the correct bus number (1 for new Pi models)
bus = smbus.SMBus(1)

RAD_TO_DEG = 57.2957795
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
LP = 0.041    	# Loop period = 41ms.   This needs to match the time it takes each loop to run
AA =  0.80      # Complementary filter constant


def writeACC(register, value):
    bus.write_byte_data(ACC_ADDRESS , register, value)
    return -1

def writeMAG(register, value):
    bus.write_byte_data(MAG_ADDRESS, register, value)
    return -1

def writeGYR(register, value):
    bus.write_byte_data(GYR_ADDRESS, register, value)
    return -1



def readACCx():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCy():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCz():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readMAGx():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
    mag_combined = (mag_l | mag_h <<8)

    return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGy():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
    mag_combined = (mag_l | mag_h <<8)

    return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
    mag_combined = (mag_l | mag_h <<8)

    return mag_combined  if mag_combined < 32768 else mag_combined - 65536



def readGYRx():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
    gyr_combined = (gyr_l | gyr_h <<8)

    return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536


def readGYRy():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
    gyr_combined = (gyr_l | gyr_h <<8)

    return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

def readGYRz():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
    gyr_combined = (gyr_l | gyr_h <<8)

    return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536



def setUp():
    #initialise the accelerometer
    writeACC(CTRL_REG1_XM, 0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
    writeACC(CTRL_REG2_XM, 0b00100000) #+/- 16G full scale

    #initialise the magnetometer
    writeMAG(CTRL_REG5_XM, 0b11110000) #Temp enable, M data rate = 50Hz
    writeMAG(CTRL_REG6_XM, 0b01100000) #+/-12gauss
    writeMAG(CTRL_REG7_XM, 0b00000000) #Continuous-conversion mode

    #initialise the gyroscope
    writeGYR(CTRL_REG1_G, 0b00001111) #Normal power mode, all axes enabled
    writeGYR(CTRL_REG4_G, 0b00110000) #Continuos update, 2000 dps full scale

    gyroXangle = 0.0
    gyroYangle = 0.0
    gyroZangle = 0.0
    CFangleX = 0.0
    CFangleY = 0.0




while True:
	a = datetime.datetime.now()

	#Read our accelerometer,gyroscope and magnetometer  values
	ACCx = readACCx()
	ACCy = readACCy()
	ACCz = readACCz()
	GYRx = readGYRx()
	GYRy = readGYRx()
	GYRz = readGYRx()
	MAGx = readMAGx()
	MAGy = readMAGy()
	MAGz = readMAGz()

	##Convert Accelerometer values to degrees
	AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
	AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG



	#Convert Gyro raw to degrees per second
	rate_gyr_x =  GYRx * G_GAIN
	rate_gyr_y =  GYRy * G_GAIN
	rate_gyr_z =  GYRz * G_GAIN


	#Calculate the angles from the gyro. LP = loop period
	gyroXangle+=rate_gyr_x*LP
	gyroYangle+=rate_gyr_y*LP
	gyroZangle+=rate_gyr_z*LP





    #Change the rotation value of the accelerometer to -/+ 180 and move the Y axis '0' point to up.
    #Two different pieces of code are used depending on how your IMU is mounted.
    #If IMU is upside down
	#
    #if AccXangle >180:
    #        AccXangle -= 360.0
    #AccYangle-=90
    #if (AccYangle >180):
    #        AccYangle -= 360.0


    #If IMU is up the correct way, use these lines
    AccXangle -= 180.0
	if AccYangle > 90:
	    AccYangle -= 270.0
	else:
        AccYangle += 90.0


    #Complementary filter used to combine the accelerometer and gyro values.
    CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
    CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle



	#Calculate heading
	heading = 180 * math.atan2(MAGy,MAGx)/M_PI

	if heading < 0:
	 	heading += 360


	#Normalize accelerometer raw values.
    accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
	accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


	#Calculate pitch and roll
	pitch = math.asin(accXnorm)
	roll = -math.asin(accYnorm/math.cos(pitch))

	#Calculate the new tilt compensated values
	magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
	magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)

	#Calculate tiles compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360

 	print ("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f \033[1;35;40m    \tCFangleX Angle %5.2f \033[1;36;40m  CFangleY Angle %5.2f \33[1;32;40m  HEADING  %5.2f \33[1;37;40m tiltCompensatedHeading %5.2f\033[0m  " % (AccXangle, AccYangle,gyroXangle,gyroYangle,gyroZangle,CFangleX,CFangleY,heading,tiltCompensatedHeading))


    time.sleep(0.03)
	b = datetime.datetime.now()
	c = b - a

	print "Loop Time |",  c.microseconds/1000,"|",
