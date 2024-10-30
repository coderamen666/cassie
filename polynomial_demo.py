from cassie.polynomial.Polynomial import *

strequ = input("Enter Your Equation: ")
equ = Polynomial.parse(strequ)
equ.combine_like_terms()
equ.differentiate()
print(equ.str_output())
'''
s1 = Polynomial.parse(input("expr 1: "))
s2 = Polynomial.parse(input("expr 2: "))
s1.multiply(s2)
print(s1.str_output())
'''
