# Finds Taylor series with symbolic differentiation
# TODO - Switch to higher precision numerical representation

from cassie.tree.nodes import *
from cassie.tree.operators import *

def disptaylor(terms):
	return ' + '.join([f'{t[0]}x^{t[1]}' if t[1] != 0 else f'{t[0]}' for t in terms])

def evaltaylor(terms, x):
	o = 0
	for t in terms:
		o += t[0] * (x ** t[1])
	return o

def simptaylor(terms):
	return [t for t in terms if t[0] != 0]

def maclaurin(etree, n):
	series = [(etree.eval({'x' : 0}), 0)]

	for n in range(1, n):
		etree = etree.differentiate('x')
		etree = etree.simplify()

		coef = etree.eval({'x' : Decimal(0)})
		if n > 1:
			for j in range(1, n + 1):
				coef /= j
		pow = n

		series.append((coef, pow))

	return series

#Example Code
#taylor = simptaylor(maclaurin(Cosine(Variable('x')), 10))
#print(disptaylor(taylor))
#print(evaltaylor(taylor, 1))
