import math

class Fraction:
	def __init__(self, top, bottom):
		self.top = int(top)
		self.bottom = int(bottom)

		if self.bottom == 0:
			raise ZeroDivisionError

		self.simplify()

	def simplify(self):
		tmp = math.gcd(self.top, self.bottom)

		self.top /= tmp
		self.bottom /= tmp

		if self.is_positive():
			self.top = int(abs(self.top))
			self.bottom = int(abs(self.bottom))
		else:
			self.top = -int(abs(self.top))
			self.bottom = int(abs(self.bottom))

	def reciprocal(self):
		return Fraction(self.bottom, self.top)

	def additive_inverse(self):
		return Fraction(-self.top, self.bottom)

	def is_positive(self):
		return (self.top > 0) == (self.bottom > 0)

	def dispstr(self):
		self.simplify()
		return f'{self.top} / {self.bottom}'

	def eval(self):
		return self.top / self.bottom

	@staticmethod
	def add(lhs, rhs):
		top = (lhs.top * rhs.bottom) + (lhs.bottom * rhs.top)
		bottom = lhs.bottom * rhs.bottom
		return Fraction(top, bottom)

	@staticmethod
	def subtract(lhs, rhs):
		top = (lhs.top * rhs.bottom) - (lhs.bottom * rhs.top)
		bottom = lhs.bottom * rhs.bottom
		return Fraction(top, bottom)

	@staticmethod
	def multiply(lhs, rhs):
		top = lhs.top * rhs.top
		bottom = lhs.bottom * rhs.bottom
		return Fraction(top, bottom)

	@staticmethod
	def divide(lhs, rhs):
		top = lhs.top*rhs.bottom
		bottom = lhs.bottom*rhs.top
		return Fraction(top, bottom)

	@staticmethod
	def parse(instr):
		if '/' in instr:
			instr = instr.replace(" ", "").split("/")
			return Fraction(instr[0], instr[1])
		else:
			return Fraction(instr, 1)
