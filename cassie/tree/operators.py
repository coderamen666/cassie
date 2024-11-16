from abc import ABC, abstractmethod
from copy import deepcopy

from cassie.tree.nodes import *

class Operator(ABC):
	@abstractmethod
	def eval(self, vdict):
		pass

class Addition(Operator):
	def __init__(self, n1, n2):
		self.node1 = n1
		self.node2 = n2

	def eval(self, vdict):
		return self.node1.eval(vdict) + self.node2.eval(vdict)

	def differentiate(self, wrt):
		n1 = deepcopy(self.node1)
		n2 = deepcopy(self.node2)
		return Addition(n1.differentiate(wrt), n2.differentiate(wrt))

	def dispstr(self):
		return f"({self.node1.dispstr()}) + ({self.node2.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		n2 = deepcopy(self.node2).simplify()

		if Constant.is_const(n1) and (not Constant.is_const(n2)):
			return Addition(n2, n1).simplify()

		if isinstance(n1, Variable) and isinstance(n2, Variable):
			if n1.name == n2.name:
				return Multiplication(Constant(2), n1)

		if isinstance(n1, Constant) and isinstance(n2, Constant):
			if (not n1.is_symbolic()) and (not n2.is_symbolic()):
				return Constant(n1.val + n2.val)
		elif isinstance(n1, Constant) and isinstance(n2, Addition):
			tmp = deepcopy(n2.node1)
			tmp2 = deepcopy(n2.node2)
			if isinstance(n2.node1, Constant):
				return Addition(
					tmp2,
					Addition(
						tmp,
						n1
					)
				).simplify()
			elif isinstance(n2.node2, Constant):
				return Addition(
					tmp,
					Addition(
						tmp2,
						n1
					)
				).simplify()
			else:
				return Addition(n1, n2)
		elif isinstance(n1, Addition) and isinstance(n2, Constant):
			tmp = deepcopy(n1.node1)
			tmp2 = deepcopy(n1.node2)
			if isinstance(n1.node1, Constant):
				return Addition(
					tmp2,
					Addition(
						tmp,
						n2
					)
				).simplify()
			elif isinstance(n1.node2, Constant):
				return Addition(
					tmp,
					Addition(
						tmp2,
						n2
					)
				).simplify()
			else:
				return Addition(n1, n2)
		elif isinstance(n1, Constant):
			if n1.val == 0:
				return n2
			else:
				return Addition(n1, n2)
		elif isinstance(n2, Constant):
			if n2.val == 0:
				return n1
			else:
				return Addition(n1, n2)

		return Addition(n1, n2)

class Subtraction(Operator):
	def __init__(self, n1, n2):
		self.node1 = n1
		self.node2 = n2

	def eval(self, vdict):
		return self.node1.eval(vdict) - self.node2.eval(vdict)

	def differentiate(self, wrt):
		n1 = deepcopy(self.node1)
		n2 = deepcopy(self.node2)
		return Subtraction(n1.differentiate(wrt), n2.differentiate(wrt))

	def dispstr(self):
		return f"({self.node1.dispstr()}) - ({self.node2.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		n2 = deepcopy(self.node2).simplify()

		if isinstance(n1, Constant) and isinstance(n2, Constant):
			if (not n1.is_symbolic()) and (not n2.is_symbolic()):
				return Constant(n1.val - n2.val)
		elif isinstance(n2, Constant):
			if n2.val == 0:
				return n1

		return Subtraction(n1, n2)

class Equals(Operator):
	def __init__(self, n1, n2):
		self.node1 = n1
		self.node2 = n2

	def eval(self, vdict):
		return self.node1.eval(vdict) == self.node2.eval(vdict)

	def differentiate(self, wrt):
		n1 = deepcopy(self.node1)
		n2 = deepcopy(self.node2)
		return Equals(n1.differentiate(wrt), n2.differentiate(wrt))

	def dispstr(self):
		return f"({self.node1.dispstr()}) = ({self.node2.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		n2 = deepcopy(self.node2).simplify()

		return Equals(n1, n2)

class Multiplication(Operator):
	def __init__(self, n1, n2):
		self.node1 = n1
		self.node2 = n2

	def eval(self, vdict):
		return self.node1.eval(vdict) * self.node2.eval(vdict)

	def differentiate(self, wrt):
		is_n1_const = Constant.is_const(self.node1)
		is_n2_const = Constant.is_const(self.node2)

		n1 = deepcopy(self.node1)
		n2 = deepcopy(self.node2)

		if is_n1_const:
			return Multiplication(n1, n2.differentiate(wrt))
		elif is_n2_const:
			return Multiplication(n2, n1.differentiate(wrt))
		else:
			return Addition(
				Multiplication(n1.differentiate(wrt), n2),
				Multiplication(n2.differentiate(wrt), n1)
			)

	def dispstr(self):
		return f"({self.node1.dispstr()})({self.node2.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		n2 = deepcopy(self.node2).simplify()

		if Constant.is_const(n2) and (not Constant.is_const(n1)):
			return Multiplication(n2, n1).simplify()

		if isinstance(n1, Constant) and isinstance(n2, Constant):
			if (not n1.is_symbolic()) and (not n2.is_symbolic()):
				return Constant(n1.val * n2.val)
		elif isinstance(n1, Constant) and isinstance(n2, Multiplication):
			tmp = deepcopy(n2.node1)
			tmp2 = deepcopy(n2.node2)
			if isinstance(n2.node1, Constant):
				return Multiplication(
					tmp2,
					Multiplication(
						tmp,
						n1
					)
				).simplify()
			elif isinstance(n2.node2, Constant):
				return Multiplication(
					tmp,
					Multiplication(
						tmp2,
						n1
					)
				).simplify()
			else:
				return Multiplication(n1, n2)
		elif isinstance(n1, Multiplication) and isinstance(n2, Constant):
			tmp = deepcopy(n1.node1)
			tmp2 = deepcopy(n1.node2)
			if isinstance(n1.node1, Constant):
				return Multiplication(
					tmp2,
					Multiplication(
						tmp,
						n2
					)
				).simplify()
			elif isinstance(n1.node2, Constant):
				return Multiplication(
					tmp,
					Multiplication(
						tmp2,
						n2
					)
				).simplify()			
			else:
				return Multiplication(n1, n2)
		if isinstance(n1, Constant):
			if n1.val == 0:
				return Constant(0)
			elif n1.val == 1:
				return n2
		if isinstance(n2, Constant):
			if n2.val == 0:
				return Constant(0)
			elif n2.val == 1:
				return n1

		return Multiplication(n1, n2)

class Division(Operator):
	def __init__(self, n1, n2):
		self.node1 = n1
		self.node2 = n2

	def eval(self, vdict):
		return self.node1.eval(vdict) / self.node2.eval(vdict)

	def differentiate(self, wrt):
		n1 = deepcopy(self.node1)
		n2 = deepcopy(self.node2)

		return Division(
				Subtraction(
					Multiplication(n1.differentiate(wrt), n2),
					Multiplication(n2.differentiate(wrt), n1)
				),
				Exponentation(n2, Constant(2))
		)

	def dispstr(self):
		return f"({self.node1.dispstr()})/({self.node2.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		n2 = deepcopy(self.node2).simplify()

		if isinstance(n2, Constant):
			if n2.val == 0:
				raise ZeroDivisionError

		if isinstance(n1, Constant) and isinstance(n2, Constant):
			if n1.val == n2.val:
				return Constant(1)

		if isinstance(n1, Constant):
			if n1.val == 0:
				return Constant(0)

		return Division(n1, n2)

class Exponentation(Operator):
	def __init__(self, n1, n2):
		self.node1 = n1
		self.node2 = n2

	def eval(self, vdict):
		return self.node1.eval(vdict) ** self.node2.eval(vdict)

	def differentiate(self, wrt):
		is_n1_const = Constant.is_const(self.node1)
		is_n2_const = Constant.is_const(self.node2)

		n1 = deepcopy(self.node1)
		n2 = deepcopy(self.node2)

		if is_n1_const and (not is_n2_const):
			# dy/dx of u = ln(b) * b^u * du/dx
			return Multiplication(
				NaturalLogarithm(n1),
				Multiplication(
					n2.differentiate(wrt),
					Exponentation(
						n1,
						n2
					)
				)
			)
		elif is_n2_const and not is_n1_const:
			return Multiplication(
				Multiplication(
					n2,
					Exponentation(
						n1,
						Subtraction(n2, Constant(1))
					),
				),
				n1.differentiate(wrt)
			)
		elif is_n1_const and is_n2_const:
			return Constant(0)
		else:
			return Exponentation(
				Constant('e'),
				Multiplication(
					n2,
					NaturalLogarithm(n1)
				)
			).differentiate(wrt)

	def dispstr(self):
		return f"({self.node1.dispstr()})^({self.node2.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		n2 = deepcopy(self.node2).simplify()

		if isinstance(n1, Constant) and isinstance(n2, Constant):
			if (not n1.is_symbolic()) and (not n2.is_symbolic()):
				return Constant(n1.val**n2.val)
			else:
				return Exponentation(n1, n2)
		elif isinstance(n2, Constant):
			if n2.val == 0:
				return Constant(1)
			elif n2.val == 1:
				return n1
			elif isinstance(n1, Exponentation):
				if n1.is_power():
					base = deepcopy(n1.node1)
					exp1 = deepcopy(n1.node2)
					exp2 = deepcopy(n2)

					return Exponentation(
						base,
						Multiplication(
							exp1,
							n2
						)
					)
						
				else:
					return Exponentation(n1, n2)
			else:
				return Exponentation(n1, n2)
		else:
			return Exponentation(n1, n2)

	def is_power(self):
		return (not Constant.is_const(self.node1))

class Negation(Operator):
	def __init__(self, n1):
		self.node1 = n1

	def eval(self, vdict):
		return 0 - self.node1.eval(vdict)

	def differentiate(self, wrt):
		n1 = deepcopy(self.node1)

		return Multiplication(
			n1.differentiate(wrt),
			Constant(-1)
		)

	def dispstr(self):
		return f"-({self.node1.dispstr})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		return Negation(n1)

class NaturalLogarithm(Operator):
	def __init__(self, n1):
		self.node1 = n1

	def eval(self, vdict):
		return math.log(self.node1.eval(vdict))

	def differentiate(self, wrt):
		is_n1_const = Constant.is_const(self.node1)
		if is_n1_const:
			return 0
		else:
			n1 = deepcopy(self.node1)
			return Division(
				n1.differentiate(wrt),
				n1
			)

	def dispstr(self):
		return f"ln({self.node1.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		return NaturalLogarithm(n1)

class Sine(Operator):
	def __init__(self, n1):
		self.node1 = n1

	def eval(self, vdict):
		return math.sin(self.node1.eval(vdict))

	def differentiate(self, wrt):
		is_n1_const = Constant.is_const(self.node1)
		if is_n1_const:
			return 0
		else:
			n1 = deepcopy(self.node1)
			return Multiplication(
				Cosine(n1),
				n1.differentiate(wrt)
			)

	def dispstr(self):
		return f"sin({self.node1.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		return Sine(n1)

class Cosine(Operator):
	def __init__(self, n1):
		self.node1 = n1

	def eval(self, vdict):
		return math.cos(self.node1.eval(vdict))

	def differentiate(self, wrt):
		is_n1_const = Constant.is_const(self.node1)
		if is_n1_const:
			return 0
		else:
			n1 = deepcopy(self.node1)
			return Multiplication(
				Multiplication(
					Sine(n1),
					Constant(-1)
				),
				n1.differentiate(wrt)
			)

	def dispstr(self):
		return f"cos({self.node1.dispstr()})"

	def simplify(self):
		n1 = deepcopy(self.node1).simplify()
		return Cosine(n1)
