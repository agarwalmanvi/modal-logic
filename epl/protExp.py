import itertools
from itertools import *
from collections import *
from obsExp import *
from modalLogic import *

class protExp:
	def __dotProt__(self):
		return DotProt(self)
	def __plusProt__(self):
		return PlusProt(self)
	def __starProt__(self):
		return StarProt(self)
	def __askProt__(self):
		return AskProt(self)

class DeltaProt(protExp):
	op = ""
	def __init__(self):
		self.name = 'd'
	def __hash__(self):
		return hash(str(self))
	def __str__(self):
		return self.name
	__repr__ = __str__
	def f(self, rho):
		return deltaObs
		
deltaProt = DeltaProt()

class EpsilonProt(protExp):
	op = ""
	def __init__(self):
		self.name = 'e'
	def __hash__(self):
		return hash(str(self))
	def __str__(self):
		return self.name
	__repr__ = __str__
	def f(self, rho):
		return epsilonObs

epsilonProt = EpsilonProt()
	
class AlphabetProt(protExp):
	op = ""
	def __init__(self, name):
		self.name = name
	def __hash__(self):
		return hash(str(self))
	def __str__(self):
		return self.name
	__repr__ = __str__
	def f(self, rho):
		return AlphabetObs(self.name)
	
class NaryOpProt(protExp):
	def __init__(self, firstChild, *args):
		self.children = []
		self.children.append(firstChild)
		for arg in args:
			self.children.append(arg)
	def __str__(self):
		tempStr = '('
		for i in range(len(self.children)):
			if i != (len(self.children)-1):
				tempStr = tempStr + str(self.children[i]) + self.op
			else:
				tempStr = tempStr + str(self.children[i])
		tempStr = tempStr + ')'
		return tempStr
	def __hash__(self):
		return hash(str(self))
		
class DotProt(NaryOpProt):
	op = "."
	def f(self, rho):
		l = []
		for child in self.children:
			l.append(child.f(rho))
		return DotObs(*l)
			
class PlusProt(NaryOpProt):
	op = "+"
	def f(self, rho):
		l = []
		for child in self.children:
			l.append(child.f(rho))
		return PlusObs(*l)
	
class UnOpProt(protExp):
	def __init__(self, child):
		self.child = child
	def __hash__(self):
		return hash(str(self))
		
class StarProt(UnOpProt):
	op = "*"
	def __str__(self):
		return '((' + str(self.child) + ')' + self.op + ')'
	def f(self, rho):
		return StarObs(self.child.f(rho))
	
class AskProt(UnOpProt):
	op = "?"
	def __str__(self):
		return '(' + self.op +'(' + str(self.child) + ')' + ')'
	def f(self, rho):
		if checkValuation(self.child, rho):
			return epsilonObs
		else:
			return deltaObs


	

	










