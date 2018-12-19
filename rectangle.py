class Rectangle:
	def __init__(self, a, b):
		self.width = max(a, b)
		self.heigh = min(a, b)
	def get_square(self):
		return self.width * self.heigh
	def get_perimetr(self):
		return 2 * (self.width + self.heigh)
if __name__ == '__main__':
	print(locals())
	print(globals())
	r = Rectangle(3, 4)
	s = r.get_square()
	p=r.get_perimetr()
	print(r, s, p)