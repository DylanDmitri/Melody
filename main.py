from itertools import product

# mod equals 0

"""
Constraint Propogation (as in Sudoku)

constraints
 - types must match
 - no loops
 - fixed number (usually 1) per input
 - operators respect left/right pairing
 - most things are mandatory includes

1. If a link has one possible value
	(must be linked, or must be unlinked)
	then put that value there.

2. Otherwise make all guesses, continuing until 
	solved or proven unsolvable.

If too many guess branches (>20) compiler error.
Return all solutions.

-------------------------------

fn (int "multiple" of:int) -> bool
	mod equals zero

parts
	mod  		(#, #) -> (#)
	equals   (2T) -> (?)
	zero     () -> (#)
	paramA   () -> (#)
	paramB   () -> (#)
	retVal   (?) -> ()

build grid
			provided
        % = 0 A B
    	  # ? # # #
t %  #  . . . . .
a %  #  . . . . .
k = 2T  . . . . .   
e R  ?  . . . . .


Check first column.
First two self-loop.
Last one has mismatched type.
Since it's a mandatory include...

			provided
        % = 0 A B
    	  # ? # # #
t %  #  0 . . . .
a %  #  0 . . . .
k = 2T  + . . . .   
e R  ?  0 . . . .

Check second column. Only 1 type matches.

			provided
        % = 0 A B
    	  # ? # # #
t %  #  0 0 . . .
a %  #  0 0 . . .
k = 2T  + 0 . . .   
e R  ?  0 + . . .

Check third to fifth column. 
There's multiple opportunities for each.

			provided
        % = 0 A B
    	  # ? # # #
t %  #  0 0 . . .
a %  #  0 0 . . .
k = 2T  + 0 . . .   
e R  ?  0 + 0 0 0

Check all rows.
Check all cols again.
Nothing has changed. (gasp)
Make a guess and percolate forward.

On reaching valid solution, run past test cases.

"""

T = 'T'

class Param:
	def __init__(self, kind, count=1):
		self.kind = kind
		self.count = count

	def could_type_match(self, other):
		return (
			self.kind == other.kind 
			or type(self.kind) == str
			or type(other.kind) == str
		)
	
	@property
	def is_generic(self):
		return type(self.kind) == str
	
	def set_generics(self, to):
		target = self.kind
		for p in self.parent.gives + self.parent.takes:
			if p.kind == target:
				p.kind = to
	
	def __repr__(self):
		return f'param: {self.count} {self.kind}'


class Atom:
	def __init__(self, takes=None, gives=None, symbol=''):
		self.takes = takes or []
		self.gives = gives or []
		self.symbol = symbol

		for t in self.takes:
			t.symbol = symbol
		for g in self.gives:
			g.symbol = symbol
	


# --------------------


class possible:
	never = 0
	maybe = 1
	yes = 5

class SynthGrid:
	@classmethod
	def from_atoms(cls, *atoms):
		self = cls()
		self.given = []
		self.taken = []

		for atom in atoms:
			for piece in atom.gives:
				piece.parent = atom
				self.given.append(piece)

			for piece in atom.takes:
				piece.parent = atom
				self.taken.append(piece)
			
		self.matches = {}

		for g,t in product(self.given, self.taken):
			self.matches[g,t] = possible.maybe
		return self

	def copy(self):
		new = SynthGrid()
		new.given = self.given
		new.taken = self.taken
		new.matches = {
			gt: self.matches[gt] for gt in
			product(self.given, self.taken)
		}
		return new
	
	"""
	matches type
	no loops
	hit target number, usually
		(0-1) or (1) or (2)
	"""

	def show_grid(self):
		print('', end='  ')
		for g in self.given:
			print(g.symbol, end=' ')
		print()

		for t in self.taken:
			print(t.symbol, end=' ')
			for g in self.given:
				print(self.matches[g, t], end=' ')
			print()

		print()
	
	def remove_mismatched_types(self):
		for g,t in product(self.given, self.taken):
			if not g.could_type_match(t):
				self.matches[g,t] = possible.never
		
	def remove_loops(self):
		for g,t in product(self.given, self.taken):
			if self.would_loop(g, t):
				self.matches[g,t] = possible.never
	
	def would_loop(self, give, take):
		seen = {give.parent}

		at = [take.parent]

		while True:
			temp = []

			for parent in at:
				if parent in seen:
					return True  # loops
				seen.add(parent)

				for g,t in product(parent.gives, self.taken):
					if self.matches[g,t] == possible.yes:
						temp.append(t.parent)
			
			at = temp
			if not at:
				return False  # exhausted, no loop
		
	def promote(self, g, t):
		if self.matches[g,t] != possible.maybe:
			return
		
		self.matches[g,t] = possible.yes
		if g.is_generic:
			g.set_generics(t.kind)

		if t.is_generic:
			t.set_generics(g.kind)


	def promote_singles(self):

		for g in self.given:
			matches = [self.matches[g,t] for t in self.taken]
			total_yes = sum(m==possible.yes for m in matches)
			total_maybe = sum(m==possible.maybe for m in matches)

			num_needed = g.count - total_yes
			num_candidates = total_maybe

			if num_needed == 0:
				# cross out solved col
				for t in self.taken:
					if self.matches[g,t] == possible.maybe:
						self.matches[g,t] = possible.never

			elif num_candidates == num_needed:
				# promote singles in col
				for t in self.taken:
					self.promote(g, t)
			

		for t in self.taken:
			matches = [self.matches[g,t] for g in self.given]
			total_yes = sum(m==possible.yes for m in matches)
			total_maybe = sum(m==possible.maybe for m in matches)

			num_needed = t.count - total_yes
			num_candidates = total_maybe

			if num_needed == 0:
				# cross out solved row
				for g in self.given:
					if self.matches[g,t] == possible.maybe:
						self.matches[g,t] = possible.never

			elif num_candidates == num_needed:
				# promote singles in row
				for g in self.given:
					self.promote(g, t)


guesses = 0
def solve(grid):
	global guesses

	while True:
		prev = list(grid.matches.values())
		grid.remove_mismatched_types()
		grid.remove_loops()
		grid.promote_singles()

		now = list(grid.matches.values())
		num_maybes = sum(m==possible.maybe for m in now)
		if num_maybes == 0:
			# todo -- 
			# if not all constraints satisfied
			#    return []
			return {tuple(grid.matches.values()): grid}  

		elif prev != now:
			continue  # stuff is changing, try another pass

		# we're stuck and need to guess
		solutions = dict()
		for g,t in product(grid.given, grid.taken):
			if grid.matches[g,t] == possible.maybe:
				guesses += 1
				cp = grid.copy()
				cp.matches[g,t] = possible.yes
				results = solve(cp)
				if results:
					solutions = solutions.update(results)
		return solutions



Mod = Atom(
	takes = [Param(int), Param(int)],
	gives = [Param(int)],
	symbol = '%',
)

# `Equals` is order-agnostic.
# It cares about 2 items simultaneusly.
Equals = Atom(
	takes = [Param(T, 2)],
	gives = [Param(bool)],
	symbol = '=',
)

Zero = Atom(
	gives = [Param(int)],
	symbol = '0'
)

ParamA = Atom(
	gives = [Param(int)],
	symbol = 'A'
)

ParamB = Atom(
	gives = [Param(int)],
	symbol = 'B'
)

RetVal = Atom(
	takes = [Param(bool)],
	symbol = 'r'
)

g = SynthGrid.from_atoms(Mod, Equals, Zero, ParamA, ParamB, RetVal)
solutions = solve(g)
print('after', guesses, 'guesses')
for s in solutions:
	print(' '.join(str(i) for i in s))




		 