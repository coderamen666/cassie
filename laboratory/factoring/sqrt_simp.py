import math

def factor_sqrt(x, n = 2):
	# Goal: Factor sqrt(x) into simplest radical form

	for i in reversed(range(math.floor(x ** (1/n)))):
		itothen = i**n
		op = x / itothen

		if (x % itothen) == 0:
			return (i, op)

	return (1, x)

print(factor_sqrt(64, 3))
