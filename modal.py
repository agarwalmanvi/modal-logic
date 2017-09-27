class Formula:
	def __not__(self):
		return Not(self)
	def __or__(self):
		return Or(self, other)
	def __and__(self):
		return And(self, other)
	def __imp__(self):
		return Imp(self, other)
	def __iff__(self):
		return Iff(self, other)
	def __box__(self):
		return Box(self)
	def __diamond__(self):
		return Diamond(self)
		
class Atom(Formula):
	#Calling as: 
	# a = Atom('a')
	def __init__(self, name):
		self.name = name
	# a = Atom('a'); b = Atom('a'); #These will have the same hash
	#I want 'a' to be the same atom in all situations, even if theyre assigned to different variable names
	def __hash__(self):
		return hash(self.name)
	#Call a.v(prop) : reduces truth to membership
	def v(self, prop):
		return self in prop
	def __str__(self):
		return str(self.name)
	__repr__ = __str__
	#Checks if two atoms with different variable names are the same
	def eq(self, other):
		return self.name == other.name
	
class BinOp(Formula):
	#extract lchild and rchild
	def __init__(self, lchild, rchild):
		self.lchild = lchild
		self.rchild = rchild
	#gives string form
	def __str__(self):
		return '(' + str(self.lchild) + self.op + str(self.rchild) + ')'
	
class And(BinOp):
	op = '&'
	def v(self, prop):
		return self.lchild.v(prop) and self.rchild.v(prop)
	
class Or(BinOp):
	op = '|'
	def v(self, prop):
		return self.lchild.v(prop) or self.rchild.v(prop)

class Imp(BinOp):
	op = '->'
	def v(self, prop):
		return not self.lchild.v(prop) or self.rchild.v(prop)
		
class Iff(BinOp):
	op = '<->'
	def v(self, prop):
		return self.lchild.v(prop) is self.rchild.v(prop)
		
class UnOp(Formula):
	def __init__(self, child):
		self.child = child
	def __str__(self):
		return '(' + self.op + str(self.child) + ')'
		
class Not(UnOp):
	op = '~'
	def v(self, prop):
		return not self.child.v(prop)
		
class Box(UnOp):
	op = '[]'
	def v(self, model, world):
		nodes = []
		for i in range(len(model.edges)):
			if model.edges[i][0] == world:
				nodes.append(model.edges[i][1])
		if not nodes:
			return True
		else:
			return all(self.child.v(model.nodes[i]) for i in nodes)
			
class Diamond(UnOp):
	op = '<>'
	def v(self, model, world):
		nodes = []
		for i in range(len(model.edges)):
			if model.edges[i][0] == world:
				nodes.append(model.edges[i][1])
		return any(self.child.v(model.nodes[i]) for i in nodes)

