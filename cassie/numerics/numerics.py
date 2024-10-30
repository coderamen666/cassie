import math

def numderiv(f, a, h = 0.001):
	return (f(a + h) - f(a - h)) / (2*h)

def numint(f, a, b, n = 100):
	tmp1 = (b - a) / n
	tmp2 = (f(a) / 2) + (f(b)/2)
	for k in range(1, n):
		tmp2 += f(a + k*tmp1)
	return tmp1 * tmp2

def slope(p1, p2):
	deltay = p2[1] - p1[1]
	deltax = p2[0] - p1[0]

	return deltay / deltax

def solve_linear(a, b, c = 0):
	# Solves ax + b = c
	return (c - b) / a

def quadratic_formula(a, b, c):
	# Solves ax^2 + bx + c = 0
	discriminant = b**2 - (4*a*c)
	if discriminant == 0:
		return -b / (2*a)
	else:
		sola = (-b + math.sqrt(discriminant)) / (2*a)
		solb = (-b - math.sqrt(discriminant)) / (2*a)
		return (sola, solb)
