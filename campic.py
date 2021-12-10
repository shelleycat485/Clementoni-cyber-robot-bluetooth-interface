import numpy, cv2, sys
from picamera import PiCamera
from time import sleep

class camdouble:

	def __init__(self):
		(xres, yres) = (320, 240)
		self.camera = PiCamera()
		self.camera.rotation=180
		self.camera.resolution = (xres, yres)
		self.camera.iso = 800
		self.im1 = numpy.empty((yres, xres, 3), dtype=numpy.uint8)
		self.im2 = numpy.empty((yres, xres, 3), dtype=numpy.uint8)
		self.imarr = [self.im1, self.im2]
		sleep(2) # allow camera to adjust

	def capture(self):
		self.camera.capture_sequence(self.imarr, 'rgb')

	def show(self):
		for i in range (0, len(self.imarr)):
			cv2.imshow(f'op{i}', self.imarr[i])
		
		cv2.waitKey(6 * 1000)

	def capresult(self):
		return (self.imarr)

	def close(self):
		self.camera.close()




