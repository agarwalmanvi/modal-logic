#.L() returns a (set of) strings
#'d' is reserved for delta and 'e' is reserved for epsilon.

import itertools
from collections import *
from pyparsing import Word, alphas, operatorPrecedence, Literal, oneOf, Suppress, nums, opAssoc, alphanums

class obsExp:
	def __dotObs__(self):
		return DotObs(self)
	def __plusObs__(self):
		return PlusObs(self)
	def __starObs__(self):
		return StarObs(self)

class DeltaObs(obsExp):
	op = ""
	def __init__(self):
		self.name = 'd'
	def __hash__(self):
		return hash(str(self))
	def __str__(self):
		return self.name
	__repr__ = __str__
		
deltaObs = DeltaObs()

class EpsilonObs(obsExp):
	op = ""
	def __init__(self):
		self.name = 'e'
	def __hash__(self):
		return hash(str(self))
	def __str__(self):
		return self.name
	__repr__ = __str__

epsilonObs = EpsilonObs()
	
class AlphabetObs(obsExp):
	op = ""
	def __init__(self, name):
		self.name = name
	def __hash__(self):
		return hash(str(self))
	def __str__(self):
		return self.name
	__repr__ = __str__

class NaryOpObs(obsExp):
	def __init__(self, firstChild, *args):
		self.children = []
		self.children.append(firstChild)
		for arg in args:
			self.children.append(arg)
	def __str__(self):
		tempStr = '('
		for i in range(len(self.children)):
			if i!=(len(self.children)-1):
				tempStr = tempStr + str(self.children[i]) + self.op
			else:
				tempStr = tempStr + str(self.children[i])
		tempStr = tempStr + ')'
		return tempStr
	def __hash__(self):
		return hash(str(self))

class DotObs(NaryOpObs):
	op = "."
			
class PlusObs(NaryOpObs):
	op = "+"
		
class UnOpObs(obsExp):
	def __init__(self, child):
		self.child = child
	def __str__(self):
		return '(' + str(self.child) + self.op + ')'
	def __hash__(self):
		return hash(str(self))
		
class StarObs(UnOpObs):
	op = '*'


###################################################### SUPPORTER FUNCTIONS ###############################################################

def simplify(expr):
	if type(expr) == DeltaObs or type(expr) == EpsilonObs or type(expr) == AlphabetObs:
		return expr
	elif type(expr) == DotObs:
		if any(isinstance(x, DeltaObs) for x in expr.children):
			return deltaObs
		else:
			if any(isinstance(x, EpsilonObs) for x in expr.children):
				expr.children = list(filter(lambda i: not(type(i) is EpsilonObs), expr.children))
			if len(expr.children) == 0:
				return epsilonObs
			elif len(expr.children) == 1:
				return simplify(expr.children[0])
			else:
				for i in range(len(expr.children)):
					expr.children[i] = simplify(expr.children[i])
				if any(isinstance(x, DeltaObs) for x in expr.children):
					return deltaObs
				if any(isinstance(x, EpsilonObs) for x in expr.children):
					expr.children = list(filter(lambda i: not(type(i) is EpsilonObs), expr.children))
				return DotObs(*expr.children)
	elif type(expr) == PlusObs:
		if any(isinstance(x, DeltaObs) for x in expr.children):
			expr.children = list(filter(lambda i: not(type(i) is DeltaObs), expr.children))
		hashList = []
		for child in expr.children:
			if hash(child) not in hashList and type(child) != DeltaObs:
				hashList.append(hash(child))
			else:
				expr.children.remove(child)
		if len(expr.children) == 0:
			return deltaObs
		elif len(expr.children) == 1:
			return simplify(expr.children[0])
		else:
			for i in range(len(expr.children)):
				expr.children[i] = simplify(expr.children[i])
			if any(isinstance(x, DeltaObs) for x in expr.children):
				expr.children = list(filter(lambda i: not(type(i) is DeltaObs), expr.children))
			expr.children = list(set(expr.children))
			hashList = []
			for child in expr.children:
				if hash(child) not in hashList and type(child) != DeltaObs:
					hashList.append(hash(child))
				else:
					expr.children.remove(child)
			if len(expr.children) == 0:
				return deltaObs
			elif len(expr.children) == 1:
				return simplify(expr.children[0])
			return PlusObs(*expr.children)
	elif type(expr) == StarObs:
		if type(expr.child) == DeltaObs:
			return deltaObs
		elif type(expr.child) == EpsilonObs:
			return epsilonObs
		elif type(expr.child) == AlphabetObs:
			return expr
		else:
			return StarObs(simplify(expr.child))
				
		
#TODO add stuff for the star operators
def makeObservation(piIn, wIn):		#pi / w
	pi = simplify(piIn)
	print(str(pi))
	w = simplify(wIn)
	print(str(w))
	if type(pi) == DeltaObs:
		if type(w) == DeltaObs:
			return epsilonObs
		else:
			return deltaObs
	elif type(pi) == EpsilonObs:
		if type(w) == EpsilonObs:
			return epsilonObs
		else:
			return deltaObs
	elif type(pi) == AlphabetObs:
		if type(w) == DeltaObs or type(w) == EpsilonObs:
			return deltaObs
		elif type(w) == AlphabetObs and hash(pi) == hash(w):
			return epsilonObs
		elif type(w) == AlphabetObs and hash(pi) != hash(w):
			return deltaObs
		elif type(w) == DotObs:
			for i in w.children:
				if w.children.index(i) == 0:
					temp = makeObservation(w, i)
				else:
					temp = makeObservation(temp, i)
			return simplify(temp)
		elif type(w) == PlusObs:
			temp = []
			for i in w.children:
				temp.append(makeObservation(pi, i))
			return simplify(PlusObs(*temp))
	elif type(pi) == DotObs:
		if type(w) == DeltaObs or type(w) == EpsilonObs:
			return deltaObs
		elif type(w) == AlphabetObs:
			temp = simplify(makeObservation(pi.children[0],w))
			if type(temp) == DeltaObs:
				return deltaObs
			else:
				pi.children.pop(0)
				return simplify(DotObs(*pi.children))
		elif type(w) == DotObs:
			for i in range(len(w.children)):
				pi.children[i] = makeObservation(pi.children[i], w.children[i])	
			return simplify(DotObs(*pi.children))
		elif type(w) == PlusObs:
			l = []
			for child in w.children:
				l.append(makeObservation(pi, child))
			return simplify(PlusObs(*l))

	elif type(pi) == PlusObs:
		if type(w) == DeltaObs or type(w) == EpsilonObs:
			return deltaObs
		elif type(w) == AlphabetObs or type(w) == DotObs or type(w) == PlusObs:
			l = []
			for i in pi.children:
				l.append(makeObservation(i,w))
			return simplify(PlusObs(*l))
