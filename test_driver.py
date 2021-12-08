# 
# tested on raspberry pi only
#
#    Copyright R Haxby 08/12/2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
from robot_btle import cyber_robot_move

def main():
	if len(sys.argv) > 1:
		robot = cyber_robot_move("03:04:05:06:0E:83")
					 # your bt device address here
	else:
		print(cyber_robot_move.helpstr)

	for argument in range (1, len(sys.argv)):
		curarg = sys.argv[argument]
		if curarg == 'sound':
			robot.sound()

		if curarg == 'ledon':
			robot.led(1)
	  
		if curarg == 'ledoff':
			robot.led(0)

		if curarg == 'help': 
			print(cyber_robot_move.helpstr)

		if curarg == 'scan':
			robot.scan()

		if curarg == 'seek':
			robot.seek()

		robot.move(curarg)
		print(curarg, end=' ')

main()
