

class Segment(object):
	"""docstring for Segment"""
	def __init__(self, x, y, len):
		self.x = x
		self.y = y
		self.len = len
		

	def update_pos(self, x, y):
		self.x = x
		self.y = y


	def show(self):
		import pyglet
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', 
			(self.x, self.y, 
			 self.x - self.len/2, self.y,
			 self.x - self.len/2, self.y - self.len/2,
			 self.x, self.y - self.len/2)))

