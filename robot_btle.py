# You may need to install bluepy, which is something like
# python3 -m pip install bluepy
# 
# tested on raspberry pi only
#
#    Copyright R Haxby 26/11/2021
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

from bluepy import btle
 
class cyber_robot_move:

	helpstr = 'argument can be: fwd back left right sound ledon ledoff scan seek\narguments can be repeated'
	cchar = ''

	def __init__(self, perstr):
		peripheral = btle.Peripheral(perstr)
		controlUUID = btle.UUID("0000fff3-0000-1000-8000-00805f9b34fb")
		remoteservice = peripheral.getServiceByUUID(controlUUID)
		self.cchar = remoteservice.getCharacteristics()

	def scan(self):
		from time import sleep
		led(1)
		sleep(0.3)
		led(0)
		# take two pics
		# diff them
		# if over threhold diff, move to centre
		# if was found, return bar else return zero as tuple (n_slices, found_slice) 

	def seek(self):
		from time import sleep
		# scan, then right 4 and scan
		scan()
		d1 = 1.25
		sleep(d1)
		for n in range(0,4):
			move( 'right')
			scan()
			sleep(d1)

		for n in range(0,4):
			move( 'left')
			scan()
			sleep(d1)

	def move(self, dd):
		dir_direction = {'fwd':b'\x31\x32\x44\x30\x53\x33',
				'back':b'\x31\x32\x44\x31\x53\x33',
				'left':b'\x31\x32\x44\x32\x53\x33',
			 	'right':b'\x31\x32\x44\x33\x53\x33'}
		n = self.cchar[1] # you get two characteristics back,
				  # I don't know what the first one is
		for d in dir_direction:
			if d == dd:
				n.write(dir_direction[dd])

	def sound(self):
		n = self.cchar[1]
		n.write(b'\x35\x36\x34\x40')

	def led(self, state):
		n = self.cchar[1]
		if state:
			n.write(b'\x37\x38\x03')
		else:
			n.write(b'\x37\x38\x04')

