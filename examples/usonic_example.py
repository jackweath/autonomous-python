import usonic

# Create new sensor object
front_sensor = usonic.newSensor(19, 26)

# Get reading until interrupted (ctrl-c)
try:
	while True:
		dist = front_sensor.getDist()

		# Output the details
		print("Distance reads", dist)
finally:
	# Clean up sensors
	usonic.cleanup()