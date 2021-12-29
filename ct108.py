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
#   GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from robot_btle import cyber_robot_move
import sys, os, time, cv2, re
import campic
g_nslices = 15
g_globseq = 0

robot = cyber_robot_move("03:04:05:06:0E:83")
camd = campic.camdouble()

class c_reposition:
	(p, target_slice, mw, nslices) = ('',0,0,0)

	def __init__(self, nslices):
		self.nslices = nslices

	def max_min_ok(self, resarr):
		av = sum (resarr) / len(resarr)
		max1 = max(resarr)
		min1 = min(resarr)
		print(f'l:{len(resarr)} av:{av} max:{max1}, min:{min1}')
		if (max1 - av < 100) and (av - min1 < 100):
			return False

		return True

	def calc_lor(self, res):
		(m, p) = (max(res), '')
		midslice = int(self.nslices/2 + 0.5)
		for i in range(0,len(res) - 1):
			if res[i] == m:
				self.target_slice = i
				p = 'fwd'
				if i > midslice + 2:
					p = 'right'
				if i < midslice - 2:
					p = 'left'

		if self.p != p: # a move wanted
			(self.p, self.mw) = (p, True)
		else:
			self.mw = False # no change to self.p because no move
		print("calc_lor target slice:", self.target_slice)
		return self.target_slice

	def send_move(self):
		global g_globseq
		if self.mw == True:
			robot.move(self.p)
			print ('send_move:', g_globseq, self.p)
			g_globseq += 1

# end of class

reposition = c_reposition(g_nslices) # slices

def target_seek(img, slices):
	nimg = cv2.integral(img)[1:,1:]
	#nimg = nimg[1:,1:]
	(rows, cols) = nimg.shape
	(vstart, vend, horiz_inc, res) = (50, rows - 1 - 100, int(cols/slices), [])
	for i in range (0, slices):
		hstart = i * horiz_inc
		hend = hstart + horiz_inc
		res.append( nimg.item(vend, hend) - nimg.item(vend, hstart)
	        	- nimg.item(vstart, hend ) + nimg.item(vstart, hstart))

	if reposition.max_min_ok(res):
		return reposition.calc_lor(res)
	else:
		return -1
	
def show_target_on_image(img, slices, hilight):
	(rows, cols, channels) = img.shape
	if hilight > 0 and hilight < (slices - 1):
		cv2.rectangle(img, (hilight * int(cols/slices),50),((hilight+1) * int(cols/slices), rows - 100),  (0, 255,0), 2)

def navigate():
	navloop = 0
	while navloop < 148:
		navloop  += 1
		camd.capture()

		(oldflag, oldimg,) = (False, None,) 
		for img in camd.capresult():
			imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			if oldflag:
				imgdiff = cv2.absdiff(imgg, oldimg)
				positionfound = target_seek (imgdiff, g_nslices)
				show_target_on_image (img, g_nslices, positionfound)
				reposition.send_move()
				if sys.argv[1] == '-D' and positionfound != -1:
					cv2.imshow("hilight", img)
					cv2.waitKey(4 * 1000)

			(oldflag, oldimg) = (True, imgg)

def main():
	if len(sys.argv) < 1:
		print ("CTxxx -d|-D")
	else:
		navigate()

main()
