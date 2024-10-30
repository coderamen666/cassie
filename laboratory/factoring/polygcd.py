import math

poly = {
	4 : 1,
	3 : -8,
	2 : 1,
}

def print_poly(p):
	out = []
	for i in p.keys():
		a = p[i]
		b = i

		if a == 0:
			continue
		elif a == 1 and b != 0:
			out.append(f'x^{i}')
		elif b == 0:
			out.append(str(a))
		elif b == 1:
			out.append(f'{a}x')
		else:
			out.append(f'{p[i]}x^{i}')
	return ' + '.join(out)

def factor_poly(p):
	gcf_coef = math.gcd(*p.values())
	gcf_power = min(*p.keys())

	gcf =  {gcf_power : gcf_coef}
	divided_poly = {}
	for power in p.keys():
		divided_poly[power - gcf_power] = p[power] / gcf_coef

	return (gcf, divided_poly)

print(print_poly(poly))
factors = factor_poly(poly)
print(f"{print_poly(factors[0])}({print_poly(factors[1])})")
