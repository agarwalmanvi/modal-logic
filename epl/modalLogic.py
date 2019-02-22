class Formula:
	def __not__(self):
		return Neg(self)
	def __or__(self):
		return Disj(self, other)
	def __and__(self):
		return Conj(self, other)
	def __imp__(self):
		return Imp(self, other)
	def __iff__(self):
		return Iff(self, other)

class Atom(Formula):
	op = ""
	def __init__(self, name):
		self.name = name
	def __hash__(self):
		return hash(self.name)
	def __str__(self):
		return str(self.name)
	__repr__ = __str__
	def eq(self, other):
		return self.name == other.name
		
	
class NaryOp(Formula):
	def __init__(self, firstChild, *args):
		self.children = []
		self.children.append(firstChild)
		for arg in args:
			self.children.append(arg)
	def __str__(self):
		tempStr = '('
		for i in range(0,len(self.children)):
			if i!=(len(self.children)-1):
				tempStr = tempStr + str(self.children[i]) + self.op
			else:
				tempStr = tempStr + str(self.children[i])
		tempStr = tempStr + ')'
		return tempStr
	
class And(NaryOp):
	op = '&'
	
class Or(NaryOp):
	op = '|'
	
class BinOp(Formula):
	def __init__(self, leftChild, rightChild):
		self.leftChild = leftChild
		self.rightChild = rightChild
	def __str__(self):
		return '(' + str(self.leftChild) + self.op + str(self.rightChild) + ')'
	
class Imp(BinOp):
	op = '->'
	
class Iff(BinOp):
	op = '<->'
	
class UnOp(Formula):
	def __init__(self, child):
		self.child = child
	def __str__(self):
		return '(' + self.op + str(self.child) + ')'
		
class Not(UnOp):
	op = '~'

class EpistemicOp(Formula):
	def __init__(self, agent, child):
		self.agent = agent
		self.child = child
	def __str__(self):
		return '(' + self.op + '_' + str(self.agent) + '_' + str(self.child) + ')'

class K(EpistemicOp):
	op = 'K'

class M(EpistemicOp):
	op = 'M'

class ObsOp(Formula):
	def __init__(self, observation, child):
		self.observation = observation
		self.child = child
	def __str__(self):
		return self.leftop + str(self.observation) + self.rightop + str(self.child)
		
class O(ObsOp):
	leftop = '['
	rightop = ']'

class ProtOp(Formula):
	def __init__(self, protocol, child):
		self.protocol = protocol
		self.child = child
	def __str__(self):
		return self.leftop + str(self.protocol) + self.rightop + str(self.child)
		
class P(ProtOp):
	leftop = '['
	rightop = ']'

#######################################SUPPORTER FUNCTIONS#############################################################################
	
def checkValuation(formula, rho):
	if type(formula) == Atom:
		for x in rho:
			if type(x) == Atom:
				if x.name == formula.name:
					return True
				else:
					return False
	elif type(formula) == Not:
		return not checkValuation(formula.child, rho)
	elif type(formula) == Or:
		return any(checkValuation(child, rho) for child in formula.children)
	elif type(formula) == And:
		return all(checkValuation(child, rho) for child in formula.children)
	elif type(formula) == Imp:
		return not checkValuation(formula.leftChild, rho) or checkValuation(formula.rightChild, rho)
	elif type(formula) == Iff:
		return checkValuation(formula.leftChild, rho) is checkValuation(formula.rightChild, rho)








