#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import math
import random


class Mouse(object):

	def __init__(self):
		self.mouse_speed = 50
		self.window_size = (1366, 768)

	def move(self, x1, y1, x2, y2, **kwargs):
		distance = abs(math.hypot(x2 - x1, y2 - y1))
		if 'mouse_speed' in kwargs.keys():
			mouse_speed = kwargs['mouse_speed']
		else:
			mouse_speed = self.mouse_speed
		if 'window_size' in kwargs.keys():
			window_size = kwargs['window_size']
		else:
			window_size = self.window_size
		window_max_distance = abs(math.hypot(window_size[0], window_size[1]))
		try:
			slope = float(y2 - y1)/float(x2 - x1)
		except ZeroDivisionError:
			slope = float('inf')
		#print abs(slope), slope
		if abs(slope) <= 1:
			steep = False
		else:
			steep = True
		if steep:
			coord_1 = y1
			coord_2 = x1
			coord1 ,coord2 = y1, y2
			if y1>y2:
				reverse = -1
			else:
				reverse = 1
		else:
			coord_1 = x1
			coord_2 = y1
			coord1, coord2 = x1, x2
			if x1 > x2:
				reverse = -1
			else:
				reverse = 1
		for index, i in enumerate(range(coord1, coord2,reverse)):
			if steep:
				x = int(((i-coord_1)/slope)+coord_2)
				y = i
				if reverse == 1:
					remaining_distance = math.hypot(x - x2, i - y2)
				else:
					remaining_distance = math.hypot(x2 - x, y2 - i)
			else:
				x = i
				y = int(((i-coord_1)*slope)+coord_2)
				if reverse == 1:
					remaining_distance = math.hypot(i - x2, y - y2)
				else:
					remaining_distance = math.hypot(x2 - i, y2 - y)
			delay = ( ((window_max_distance - distance)/window_max_distance) * (distance - remaining_distance)/distance ) * 0.001
			delay = delay + 0.0001
			try:
				delay = delay / (mouse_speed * 0.01)
			except ZeroDivisionError:
				delay = 0 
			yield [x , y , mouse_speed, delay]
			time.sleep(delay)

	def click(self, x, y):
		pass
