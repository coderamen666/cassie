def factorial_factors(n):
	if n == 0:
		return [1]
	elif n < 0:
		return None
	else:
		return [i for i in range(1, n + 1)]

def ltodict(l):
	d = {}
	for item in l:
		if item not in d:
			d[item] = 0
		d[item] += 1
	return d

def muldict(d):
	out = 1
	for i in d:
		out *= pow(i, d[i])
	return out

def bincoef(n, k):
	# Computes (n!) / ((k!)(n - k!))
	# Programmed to avoid overflows

	top = ltodict(factorial_factors(n)) # n!
	bottom = ltodict(factorial_factors(k) + factorial_factors(n - k)) # k!(n - k)!
	tmp = []

	print(top, bottom)

	for fact in top:
		if fact in bottom:
			if top[fact] >= bottom[fact]:
				top[fact] -= bottom[fact]
				bottom.pop(fact, None)
			else:
				bottom[fact] -= top[fact]
				top[fact] = 0

		if top[fact] == 0:
			tmp.append(fact)

	for key in tmp:
		top.pop(key, None)

	print(top, bottom)

	ans = muldict(top)
	for fact in bottom:
		ans = ans // pow(fact, bottom[fact])
	return ans

'''
def bincoef(n, k):
	return factorial(n) / (factorial(k) * factorial(n - k))
'''

def bintheorem(n):
	terms = []
	for k in range(n + 1):
		coef = bincoef(n, k)
		terms.append((coef, n - k, k))
	return terms

def dispstr(terms):
	strterms = []
	for term in terms:
		strterm = []
		strcoef = []

		coef = term[0]
		if coef == 0:
			continue
		elif coef != 1:
			strterm.append(str(coef))

		for i in [('x', term[1]), ('y', term[2])]:
			var, pow = i
			if pow == 0:
				continue
			elif pow == 1:
				strterm.append(var)
			else:
				strterm.append(f'{var}^{pow}')

		strterms.append(''.join(strterm))
	return ' + '.join(strterms)

def eval(x, y, terms):
	out = 0
	for term in terms:
		out += term[0] * (x ** term[1]) * (y ** term[2])
	return out

def pascals_triangle(n):
	for i in range(0, n + 1):
		for _ in range(i + 1):
			print(bincoef(i, _), end=' ')
		print()
'''
for n in range(1, 100):
	equ = bintheorem(n)
	print(f"Computing 1.001^{n}")
	print("Symbolic Expansion:", dispstr(equ))
	print("FP Math:", (1.001)**n)
	print("Symbolics:", eval(1, .001, equ))
	print()
'''
#print(pascals_triangle(20))

print(bincoef(49, 25))
