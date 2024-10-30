import math

def prime_factorize(n):
	out = []
	while (n % 2) == 0:
		out.append(2)
		n /= 2

	for i in range(3, int(math.sqrt(n)) + 1, 2):
		while (n % i) == 0:
			out.append(i)
			n /= i

	if n > 2:
		out.append(int(n))

	return out

#for i in range(2, 9000000):
#	print(f'{i}: {prime_factorize(i)}')

i = 3**30
print(f'{i}: {prime_factorize(i)}')
