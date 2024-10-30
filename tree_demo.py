from cassie.tree.nodes import *
from cassie.tree.operators import *

from cassie.parsers.ReversePolishParser import ReversePolishParser as rpnparse

if __name__=="__main__":
	expr_tree = rpnparse.parse(input(">"))
	if expr_tree != None:
		simp = expr_tree.simplify()
		dsimp = simp.differentiate('x')
		for i in range(5):
			dsimp = dsimp.simplify()
			print(f"d/dx of {simp.dispstr()} is: {dsimp.dispstr()}")
	else:
		print("Invalid Input")
