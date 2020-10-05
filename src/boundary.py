

class Boundary(object):
	"""docstring for Boundary"""

	def __init__(self, x1, y1, x2, y2):
		self.a = [x1, y1]
		self.b = [x2, y2]
		

	def show(self):
		import pyglet
		pyglet.gl.glLineWidth(2)
		pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (self.a[0], self.a[1], self.b[0], self.b[1])))
