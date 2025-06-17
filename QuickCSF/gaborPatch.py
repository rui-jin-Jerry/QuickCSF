# -*- coding: utf-8 -*
'''Gabor patches as QImages'''

import math

from qtpy import QtGui

class GaborPatchImage(QtGui.QImage):
	'''Create a gabor patch'''

	def __init__(self,
		size=100,
		orientation=45,
		gaussianStd=None,
		frequency=.1,
		phase=math.tau/4,
		color1=QtGui.QColor(255, 255, 255),
		color2=QtGui.QColor(0, 0, 0)
	):
		'''Create a gabor patch QImage'''
		self.size = int(size)  # Ensure it's an integer
		super().__init__(self.size, self.size, QtGui.QImage.Format_ARGB32)

		self.orientation = orientation
		self.gaussianStd = gaussianStd if gaussianStd is not None else self.size / 8
		self.frequency = frequency
		self.phase = phase
		self.color1 = color1
		self.color2 = color2

		self.setPixels()

	def setPixels(self):
		# convert orientation degrees to radians
		orientation_rad = (self.orientation + 90) * math.tau / 360

		# normalize size to a Gaussian scale
		scaled_size = self.size / self.gaussianStd

		color1 = self.color1.getRgb()
		color2 = self.color2.getRgb()

		for rx in range(self.size):
			for ry in range(self.size):
				dx = rx - 0.5 * self.size
				dy = ry - 0.5 * self.size

				t = math.atan2(dy, dx) + orientation_rad
				r = math.sqrt(dx * dx + dy * dy)

				x = r * math.cos(t)
				y = r * math.sin(t)

				amp = 0.5 + 0.5 * math.cos(self.phase + math.tau * (x * self.frequency))
				f = math.exp(-0.5 * (x / self.gaussianStd) ** 2 - 0.5 * (y / self.gaussianStd) ** 2)

				r_val = color1[0] * amp + color2[0] * (1 - amp)
				g_val = color1[1] * amp + color2[1] * (1 - amp)
				b_val = color1[2] * amp + color2[2] * (1 - amp)
				a_val = f * (color1[3] * amp + color2[3] * (1 - amp))

				self.setPixel(rx, ry, QtGui.qRgba(int(r_val), int(g_val), int(b_val), int(a_val)))


	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return f'{self.__class__.__name__}(' + str(vars(self)) + ')'


class ContrastGaborPatchImage(GaborPatchImage):
	def __init__(self, contrast=1.0, *args, **kwargs):
		'''Create a black-and-white gabor patch QImage by specifiying contrast

			Args:
				contrast: a value between 0-1 indicating how much contrast should be present between dark and light bands
		'''

		self.contrast = contrast

		# Calculate luminance values in the 0–255 range
		# max_intensity = int(round(255 * contrast))
		#color1 = QtGui.QColor(max_intensity, 0, 0)
		#color2 = QtGui.QColor(0, max_intensity, 0)
		high_luminance = int(round(255 * (0.5 + 0.5 * contrast)))
		low_luminance = int(round(255 * (0.5 - 0.5 * contrast)))

		# Use integer RGB values in QColor
		color1 = QtGui.QColor(high_luminance, high_luminance, high_luminance)
		color2 = QtGui.QColor(low_luminance, low_luminance, low_luminance)

		super().__init__(color1=color1, color2=color2, *args, **kwargs)

