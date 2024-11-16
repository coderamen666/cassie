class PolynomialTerm:
	def __init__(self, coef, power):
		self.coef = coef
		self.power = power
		self.nullterm = (self.power == 0) and (self.coef == 0)

	def eval(self, num):
		if self.nullterm:
			return 0
		return self.coef * (num**self.power)

	def differentiate(self):
		if (self.power == 0) or (self.coef == 0):
			self.nullterm = True
			self.power = 0
			self.coef = 0
			return
		self.coef *= self.power
		self.power -= 1

	def integrate(self):
		self.power += 1
		self.coef /= self.power

	def multiply(self, otherterm):
		self.coef *= otherterm.coef
		self.power += otherterm.power

	def str_output(self):
		strcoef = str(self.coef) if self.coef != 1 else ""

		if (self.power == 0) and (self.coef == 0):
			return '0'
		if self.power == 1:
			return f'{strcoef}x'
		elif self.power == 0:
			return str(self.coef)
		elif self.power < 0:
			abspower = abs(self.power)
			if abspower != 1:
				return f'{strcoef}/(x^{abspower})'
			else:
				return f'{strcoef}/x'
		else:
			return f'{strcoef}x^{self.power}'

	def degree(self):
		return self.power if self.power >= 0 else None

	@staticmethod
	def parse(strterm):
		strterm = strterm.replace("*", "")
		if (len(strterm) == 1) and strterm.isalpha():
			return PolynomialTerm(1, 1) 

		try:
			coef = float(strterm)
			power = 0
			return PolynomialTerm(coef, power)
		except ValueError:
			if '^' in strterm:
				tmp = strterm.split('^')
				power = float(tmp[-1])
				try:
					coef = float(tmp[0][:-1])
				except:
					coef = 1
			else:
				power = 1
				coef = float(strterm[:-1])

		return PolynomialTerm(coef, power)
