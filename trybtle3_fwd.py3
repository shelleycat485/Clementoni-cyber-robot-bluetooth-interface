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
import sys

helpstr = 'argument can be: fwd back left right sound ledon ledoff\narguments can be repeated'
 
dir_direction = {'fwd':b'\x31\x32\x44\x30\x53\x33',
                 'back':b'\x31\x32\x44\x31\x53\x33',
                 'left':b'\x31\x32\x44\x32\x53\x33',
                 'right':b'\x31\x32\x44\x33\x53\x33'}

def move(characteristics, dd):
  n = characteristics[1] # you get two characteristics back,
                         # I don't know what the first one is
  for d in dir_direction:
    if d == dd:
      n.write(dir_direction[dd])

def sound(characteristics):
  n = characteristics[1]
  n.write(b'\x35\x36\x34\x40')

def led(characteristics, state):
  n = characteristics[1]
  if state:
    n.write(b'\x37\x38\x03')
  else:
    n.write(b'\x37\x38\x04')

dev = btle.Peripheral("03:04:05:06:0E:83") # your bt device address here

controlUUID = btle.UUID("0000fff3-0000-1000-8000-00805f9b34fb")

if len(sys.argv) > 1:
  remoteservice = dev.getServiceByUUID(controlUUID)
  controlchar = remoteservice.getCharacteristics()
else:
   print(helpstr)

for argument in range (1, len(sys.argv)):
  curarg = sys.argv[argument]
  move(controlchar, curarg)
  print(curarg, end='')
  if curarg == 'sound':
    sound(controlchar)

  if curarg == 'ledon':
    led(controlchar, 1)
  
  if curarg == 'ledoff':
    led(controlchar,0)

  if curarg.find('help') != -1:
    print(helpstr)


