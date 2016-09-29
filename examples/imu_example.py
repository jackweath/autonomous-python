from imu import *
import datetime

while True:
	a = datetime.datetime.now()
	gyroXangle = 0.0
	gyroYangle = 0.0
	gyroZangle = 0.0
	CFangleX = 0.0
	CFangleY = 0.0
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
