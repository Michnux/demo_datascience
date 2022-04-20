



# conventions:

# image coordinates:
# - Origin: top left
# - x axis: horizontal towards right. Min=0, Max=1.
# - y axis: vertical towards down. Min=0, Max=1.

# (x1,y1) top left point of bbox
# (x2,y2) bottom right point of bbox
# (x,y) center of bbox


class bbox_x1y1wh:

	x1: float
	y1: float
	w: float
	h: float

	def __init__(self, x1, y1, w, h):
		self.x1 = x1
		self.y1 = y1
		self.w = w
		self.h = h

	def x1y1wh(self):
		return self

	def xywh(self):
		x = self.x1 + self.w/2
		y = self.y1 + self.h/2
		w = self.w
		h = self.h
		return bbox_xywh(x, y, w, h)
	
	def x1y1x2y2(self):
		x1 = self.x1
		y1 = self.y1
		x2 = self.x1 + self.w
		y2 = self.y1 + self.h
		return bbox_x1y1x2y2(x1, y1, x2, y2)



class bbox_xywh:

	x: float
	y: float
	w: float
	h: float

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def x1y1wh(self):
		x1 = self.x - self.w/2
		y1 = self.y - self.h/2
		w = self.w
		h = self.h
		return bbox_x1y1wh(x1, y1, w, h)

	def xywh(self):
		return self

	def x1y1x2y2(self):
		x1 = self.x - self.w/2
		y1 = self.y - self.h/2
		x2 = self.x + self.w/2
		y2 = self.y + self.h/2
		return bbox_x1y1x2y2(x1, y1, x2, y2)



class bbox_x1y1x2y2:

	x1: float
	y1: float
	x2: float
	y2: float

	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

	def x1y1wh(self):
		x1 = self.x1
		y1 = self.y1
		w = self.x2 - self.x1
		h = self.y2 -self.y1
		return bbox_x1y1wh(x1, y1, w, h)
	
	def xywh(self):
		x = (self.x1 + self.x2)/2
		y = (self.y1 + self.y2)/2
		w = self.x2 - self.x1
		h = self.y2 -self.y1
		return bbox_xywh(x, y, w, h)

	def x1y1x2y2(self):
		return self