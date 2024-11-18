# Subroutines to manipulate polynomials
# The polynomials are stored as python dictionaries
# The powers are the keys, and the coefficients are the values

import math

def polyclean(p): # Cleans out powers with null coefficients
	if p == {}:
		return {}
	else:
		out = {}
		for power in p:
			if p[power] != 0:
				out[power] = p[power]
		return out

def polyzero(p): # Checks if polynomial is zero
	tmp = polyclean(p)
	return tmp == {}

def polyeq(p1, p2): # Checks if 2 polynomials are equal
	p1, p2 = polyclean(p1), polyclean(p2)
	return polyzero(subpolys(p1, p2))

def degree(poly): # Finds the highest power of the polynomial
	poly = polyclean(poly)
	return 0 if polyzero(poly) else max(poly.keys())

def lcoef(poly): # Finds leading coefficient
	return poly[degree(poly)]

def negate(poly): # Additive inverse function
	poly = polyclean(poly)
	if polyzero(poly):
		return {}
	result = {}
	for power in poly:
		result[power] = -poly[power]
	return polyclean(result)

def evalpoly(poly, x): # "Plugs in" value into polynomial
	poly = polyclean(poly)
	if polyzero(poly):
		return 0
	out = 0
	for power in poly:
		out += poly[power] * (x ** power)
	return out

def addpolys(polys): # Adds a list of polynomials together
	result = {}
	for poly in polys:
		poly = polyclean(poly)
		if polyzero(poly):
			continue
		for power in poly:
			if power not in result:
				result[power] = 0
			result[power] += poly[power]
	return polyclean(result)

def subpolys(p1, p2): # Subtracts 2 polynomials
	p1, p2 = polyclean(p1), polyclean(p2)
	result = dict(p1)
	if polyzero(p2):
		return result
	elif polyzero(p1):
		return negate(p2)
	else:
		for power in p2:
			if power not in result:
				result[power] = 0
			result[power] -= p2[power]
		return polyclean(result)

def distmon(poly, monomial): # Distributes monomial across polynomial
	poly = polyclean(poly)
	if polyzero(poly) or polyzero(monomial):
		return {}
	result = {}
	monomial_pow = list(monomial.keys())[0]
	monomial_coef = monomial[monomial_pow]
	for power in poly:
		new_power = power + monomial_pow
		new_coef = poly[power] * monomial_coef
		result[new_power] = new_coef
	return polyclean(result)

def divmon(poly, monomial): # Divides polynomial by monomial
	poly = polyclean(poly)
	if polyzero(poly):
		return {}
	elif polyzero(monomial):
		raise ZeroDivisionError
	else:
		result = {}
		monomial_pow = list(monomial.keys())[0]
		monomial_coef = monomial[monomial_pow]
		for power in poly:
			new_power = power - monomial_pow
			new_coef = poly[power] / monomial_coef
			result[new_power] = new_coef
		return polyclean(result)

def polymult(p1, p2): # Multiplies 2 polynomials together
	p1, p2 = polyclean(p1), polyclean(p2)
	if polyzero(p1) or polyzero(p2):
		return {}
	else:
		intermediates = []
		for power in p2:
			monomial = {power : p2[power]}
			intermediates.append(distmon(p1, monomial))
		return addpolys(intermediates)

def scalepoly(poly, s): # Multiplies polynomial by number
	out = {}
	poly = polyclean(poly)

	for power in poly:
		out[power] = s * poly[power]

	return out

def diffpoly(poly): # Finds the derivative of a given polynomial
	poly = polyclean(poly)
	out = {}
	if polyzero(poly):
		return {}
	for power in poly:
		if power == 0:
			continue
		else:
			out[power - 1] = poly[power] * power
	return polyclean(out)

def intpoly(poly, initial_value = None): # Finds the integral of a polynomial
	poly = polyclean(poly)
	out = {}
	if not polyzero(poly):
		for power in poly:
			if power == -1:
				raise NotImplementedError
			else:
				out[power + 1] = poly[power] / (power + 1)

	if initial_value != None:
		initx = initial_value[0]
		inity = initial_value[1]
		out[0] = inity - evalpoly(out, initx)
	return polyclean(out)

def dispstr(poly): # Displays polynomials in a pretty format
	poly = polyclean(poly)
	strterms = []
	for power in sorted(poly.keys(), reverse=True):
		if poly[power] == 0:
			continue
		elif power == 0:
			strterms.append(str(poly[power]))
		elif (poly[power] == 1) and (power == 1):
			strterms.append('x')
		elif poly[power] == 1:
			strterms.append(f"x^{power}")
		elif power == 1:
			strterms.append(f"{poly[power]}x")
		else:
			strterms.append(f"{poly[power]}x^{power}")
	return ' + '.join(strterms)

def _polydiv(n, d): # Extended synthetic division (internal alg.)
	out = list(n)
	normalizer = d[0]
	for i in range(len(n) - len(d) + 1):
		out[i] /= normalizer
		coef = out[i]
		if coef != 0:
			for j in range(1, len(d)):
				out[i + j] += -d[j] * coef
	separator = 1 - len(d)
	return out[:separator], out[separator:]

def _ltodict(l): # Internal function for dividing algorithm
	out = {}
	for i in range(0, len(l)):
		out[i] = l[i]
	return out

def _dicttol(d): # Another internal function
	l = [0 for i in range(0, max(d.keys()) + 1)]
	for key in d:
		l[key] = d[key]
	return l

def polydiv(n, d): # User facing division function
	n, d = polyclean(n), polyclean(d)
	for poly in [n, d]:
		for power in poly:
			if power < 0:
				raise NotImplementedError

	if polyzero(n):
		return {}
	elif polyzero(d):
		raise ZeroDivisionError
	else:
		_n, _d = _dicttol(n)[::-1], _dicttol(d)[::-1]
		q, r = _polydiv(_n, _d)
		return (polyclean(_ltodict(q[::-1])), polyclean(_ltodict(r[::-1])))

def factor_out(poly): # Factors out monomial
	tmp = {min(poly.keys()) : math.gcd(*poly.values())}
	return (tmp, divmon(poly, tmp))

def factors(n1): # Finds the factors of a positive number
	n = int(n1)
	if n == 1:
		return [1]
	return [i for i in range(1, n) if (n%i)==0]

def _polyfactor(poly): # Finds linear factors with the rational root theorem
	poly = polyclean(poly)
	cterm = poly[0] if 0 in poly.keys() else 0
	lc = lcoef(poly)

	if cterm == 0:
		return (poly, )
	else:
		cfacts = factors(abs(cterm))
		lcfacts = factors(abs(lc))

		candidates = set()
		for cfact in cfacts:
			for lcfact in lcfacts:
				candidates.add(cfact / lcfact)
				candidates.add(-cfact / lcfact)
		candidates = list(candidates)
		zeros = [i for i in candidates if evalpoly(poly, i)==0]

		facts = [{1:1, 0 : -zero} for zero in zeros]
		if facts == []:
			return (poly, )
		tmp = {0:1}
		for factor in facts:
			tmp = polymult(factor, tmp)
		lfq, lfr = polydiv(poly, tmp)
		if lfq != {0:1}:
			return (*facts, lfq)
		else:
			return tuple(facts)

def polyfactor(poly): # User facing factoring function
	f1, p2 = factor_out(poly)
	facts = list(_polyfactor(p2))
	facts = list(facts) + [f1]
	return facts

def factlist(facts):
	out = ""
	for fact in facts:
		out += f'({dispstr(fact)})'
	return out

def parseterm(strterm):
	strterm = strterm.replace("*", "")
	if (len(strterm) == 1) and strterm.isalpha():
		return {1 : 1}

	try:
		coef = int(strterm)
		power = 0
		return  {power : coef}
	except ValueError:
		if '^' in strterm:
			tmp = strterm.split('^')
			power = int(tmp[-1])
			try:
				coef = int(tmp[0][:-1])
			except:
				coef = 1
		else:
			power = 1
			coef = int(strterm[:-1])

	return {power : coef}

def parseequ(equ):
	try:
		return addpolys([parseterm(strterm.replace(" ", '')) for strterm in equ.replace('-', '+-').split("+")])
	except:
		return addpolys([parseterm(strterm.replace(" ", '')) for strterm in equ.split("+")])

p = parseequ(input())
p = {5: 1, 4: -1, 3: -101, 2: 189, 1: 828, 0: -1620}
fs = polyfactor(p)
print(factlist(fs))
