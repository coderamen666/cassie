from cassie.polynomial.PolynomialTerm import *
import copy

class Polynomial:
	def __init__(self, terms):
		self.terms = terms
		self.combine_like_terms()

	def eval(self, inp):
		return sum([term.eval(inp) for term in self.terms])

	def differentiate(self):
		self.combine_like_terms()
		for term in self.terms:
			term.differentiate()

	def integrate(self):
		self.combine_like_terms()
		for term in self.terms:
			term.integrate()

	def defintegral(self, a, b):
		c = Polynomial(copy.deepcopy(self.terms))
		c.integrate()

		if a > b:
			a, b = b, a

		return c.eval(b) - c.eval(a)

	def distribute_term(self, dterm):
		self.combine_like_terms()
		for term in self.terms:
			term.multiply(dterm)

	def distribute_term_and_copy(self, dterm):
		new_poly = Polynomial(copy.deepcopy(self.terms))
		new_poly.distribute_term(dterm)
		return new_poly

	def str_output(self):
		self.combine_like_terms()

		if (len(self.terms) == 1) and (self.terms[0].nullterm):
			return '0'

		strterms = [term.str_output() for term in self.terms if (not term.nullterm)]
		s = ""
		for i in range(len(strterms)):
			if i == 0:
				s += strterms[i]
			else:
				s += f" + {strterms[i]}"

		return s.replace("+ -", "- ")

	def combine_like_terms(self):
		new_terms = dict()
		for i in range(len(self.terms)):
			term = self.terms[i]
			power = term.power
			if power in new_terms.keys():
				new_terms[power] += term.coef
			else:
				new_terms[power] = term.coef
		self.terms = [PolynomialTerm(new_terms[power], power) for power in new_terms.keys()]
		self.terms.sort(key=lambda x: x.power, reverse=True)

	def add(self, otherpoly):
		self.terms += otherpoly.terms
		self.combine_like_terms()

	def multiply(self, otherpoly):
		terms = []
		for term in otherpoly.terms:
			npoly = self.distribute_term_and_copy(term)
			terms += npoly.terms
		self.terms = terms
		self.combine_like_terms()

	@staticmethod
	def parse(equ):
		try:
			return Polynomial([PolynomialTerm.parse(strterm.replace(" ", '')) for strterm in equ.replace('-', '+-').split("+")])
		except:
			return Polynomial([PolynomialTerm.parse(strterm.replace(" ", '')) for strterm in equ.split("+")])
