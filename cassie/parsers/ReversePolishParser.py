from cassie.tree.nodes import *
from cassie.tree.operators import *

class ReversePolishParser:
	@staticmethod
	def parse(str):
		tokens = str.split(' ')
		operand_stack = []
		variables = 'xyz'
		try:
			for token in tokens:
				if token == '+':
					rhs = operand_stack.pop()
					lhs = operand_stack.pop()

					operand_stack.append(Addition(lhs, rhs))
				elif token == '-':
					rhs = operand_stack.pop()
					lhs = operand_stack.pop()

					operand_stack.append(Subtraction(lhs, rhs))
				elif token == '*':
					rhs = operand_stack.pop()
					lhs = operand_stack.pop()

					operand_stack.append(Multiplication(lhs, rhs))
				elif token == '/':
					rhs = operand_stack.pop()
					lhs = operand_stack.pop()

					operand_stack.append(Division(lhs, rhs))
				elif token == '^':
					rhs = operand_stack.pop()
					lhs = operand_stack.pop()

					operand_stack.append(Exponentation(lhs, rhs))
				elif token in variables:
					operand_stack.append(Variable(token))
				else:
					operand_stack.append(Constant(token))

			if len(operand_stack) == 1:
				return operand_stack[0]
		except Exception as e:
			print(e)
			return None
