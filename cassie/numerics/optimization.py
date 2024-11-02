# Optimizes a continuous function using finite differences

import math

def ucoptim(f, guess, step = 0.01, eps = 1e-10, h = 0.001, max_iters = 1000):
	optim_inp = guess
	df = (f(optim_inp + h) - f(optim_inp - h)) / (2*h)
	iters = 0

	while abs(df) > eps:
		if iters > max_iters:
			return None

		df = (f(optim_inp + h) - f(optim_inp - h)) / (2*h)
		optim_inp -= abs(step * df)
		iters += 1

	return (optim_inp, f(optim_inp)) if (abs(optim_inp) > eps) else (0, f(0))

def coptim(f, rg, min = True, step = 0.01, eps = 1e-10, h = 0.001, max_iters = 10000, multout = False):
	candidates = [(i, f(i)) for i in rg]
	for i in range(math.floor(rg[0] - 1), math.ceil(rg[1] + 1)):
		candidate = ucoptim(f, i, step, eps, h, max_iters)
		if (candidate != None) and (candidate not in candidates):
			if (candidate[0] >= rg[0]) and (candidate[0] <= rg[1]):
				candidates.append(candidate)

	if multout:
		best_candidates = [candidates[0]]
		for candidate in candidates[1:]:
			if candidate[1] == best_candidates[0][1]:
				best_candidates.append(candidate)
				continue
			if min:
				if candidate[1] < best_candidates[0][1]:
					best_candidates = [candidate]
					continue
			else:
				if candidate[1] > best_candidates[0][1]:
					best_candidates = [candidate]
					continue

			return best_candidates
	else:
		best_candidate = candidates[0]
		for candidate in candidates[1:]:
			if min:
				if candidate[1] < best_candidate[1]:
					best_candidate = candidate
					continue
			else:
				if candidate[1] > best_candidate[1]:
					best_candidate = candidate
					continue
		return best_candidate
