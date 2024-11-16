from abc import ABC, abstractmethod
import math
from decimal import Decimal
from copy import deepcopy

class Node(ABC):
	@abstractmethod
	def eval(self, vdict):
		pass

	@abstractmethod
	def differentiate(self, wrt):
		pass

	@abstractmethod
	def dispstr(self):
		pass

	@abstractmethod
	def simplify(self):
		pass

class Constant(Node):
	def __init__(self, val):
		try:
			self.val = Decimal(val)
			self.irrational = False
			self.symbolic_constant = False
		except:
			self.val = val
			self.irrational = (val == 'e') or (val == 'pi') or ("sqrt" in val) or ("ln" in val)
			self.symbolic_constant = True

	def eval(self, vdict):
		if not self.irrational:
			return self.val
		elif self.val == 'e':
			return math.e
		elif self.val == 'pi':
			return math.pi

	def differentiate(self, wrt):
		return Constant(0)

	def dispstr(self):
		return str(self.val)

	@staticmethod
	def is_const(x):
		if isinstance(x, Constant):
			return True
		elif isinstance(x, Variable):
			return False
		else:
			return Constant.is_const(x.node1) and Constant.is_const(x.node2)

	def simplify(self):
		return deepcopy(self)

	def is_symbolic(self):
		return self.symbolic_constant

class Variable(Node):
	def __init__(self, name):
		self.name = name

	def differentiate(self, wrt):
		if wrt == self.name:
			return Constant(1)
		else:
			return VariablePrime(self.name, 1, wrt)

	def eval(self, vdict):
		if self.name in vdict:
			return vdict[self.name]
		return 0

	def dispstr(self):
		return self.name

	def simplify(self):
		return deepcopy(self)

class VariablePrime(Variable):
	def __init__(self, name, order, wrt):
		super().__init__(name)
		self.order = order
		self.wrt = wrt

	def differentiate(self, wrt):
		if self.wrt == wrt:
			cp = deepcopy(self)
			cp.order += 1
		else:
			raise NotImplementedError

	def eval(self, vdict):
		raise NotImplementedError

	def dispstr(self):
		o = str(self.order) if self.order != 1 else ""
		return f"(d{o}{self.name}/d{self.wrt}{o})"

	def simplify(self):
		return deepcopy(self)
