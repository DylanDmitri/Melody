from itertools import permutations

class Header:
	pass


class QTerm: 
	# a superposition of many terms
	...

class Term:
	def __repr__(self):
		return self.__class__.__name__
	
	def output_for(self, iteration):
		...

class Mod(Term):
	params = [int, int]
	output = int

	def output_for(self, params, iteration):
		return params[0] % params[1]

class Equals(Term):
	params = [int, int]
	output = bool

	def output_for(self, params, iteration):
		return params[0] == params[1]

class Zero(Term):
	params = []
	output = int

	def output_for(self, params, iteration):
		return 0

class ParamA(Term):
	params = []
	output = int

	def output_for(self, params, iteration):
		return [3, 9][iteration]

class ParamB(Term):
	params = []
	output = int

	def output_for(self, params, iteration):
		return [9, 3][iteration]


def check(ordering):
	# trying to discover the lisp ordering of elements
	# such that there are no loose ends
	stack = []
	for term in ordering:
		num_expected = len(term.params)
		if len(stack) < num_expected:
			return False
		
		popped = [stack.pop() for _ in range(num_expected)]
		if popped != term.params:
			return False

		stack.append(term.output)
	return True


def run(ordering, iteration=0):
	stack = []
	for term in ordering:
		num_expected = len(term.params)
		assert num_expected <= len(stack) 
		
		popped = [stack.pop() for _ in range(num_expected)]
		result = term.output_for(popped, iteration)

		assert isinstance(result, term.output)
		stack.append(result)

	return stack

def running_catch(ordering, outputs):
	print(ordering)
	for i, out in enumerate(outputs):
		try:
			result = run(ordering, iteration=i)
			# print(result, '=?=', expected)
			if result != out:
				return False
		except:
			return False
		print(result, expected)
	return True




terms = [ParamA(), ParamB(), Mod(), Zero(), Equals()]

print(run(terms))


# whreer the header is a header object
#     lines
#     groups
#     each i with type, name, prep, literal
#     start with only one literal per

# body
#     lines
#     split each line into terms
#     lookup terms

# tests

