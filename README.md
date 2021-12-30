
# Intro
These are bluetooth codes for the Clementoni Cyber Robot, as far as I have found out.  

## Method
I used an Adafruit Bluetooth LE Sniffer to see how the app communicated with the robot.  This was then verified using a Raspberry Pi 3 with a BT adapter, scanning for the LE address using hcitool, then testing commands using gatttool.

## Python Program
This was to check the commands worked

campic.py Take pairs of pictures and process for differeces

robot_btle.py class to allow control of robot

test_driver.py allows testing the robot_btle class above

trybtle3_fwd.py first try of program to access bt directly, sending commands from the command line

ct108.py get robot moving towards movement, using the library classes.

ct107.py earlier version of the same, historical only


