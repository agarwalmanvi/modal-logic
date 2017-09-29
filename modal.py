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
	op = ""
	#Calling as: 
	# a = Atom('a')
	def __init__(self, name):
		self.name = name
	# a = Atom('a'); b = Atom('a'); #These will have the same hash
	#I want 'a' to be the same atom in all situations, even if theyre assigned to different variable names
	def __hash__(self):
		return hash(self.name)
	#Call a.v(prop) : reduces truth to membership
	def v(self, model, world):
		return self in model.nodes[world]
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
	def v(self, model, world):
		return self.lchild.v(model, world) and self.rchild.v(model, world)
	
class Or(BinOp):
	op = '|'
	def v(self, model, world):
		return self.lchild.v(model, world) or self.rchild.v(model, world)

class Imp(BinOp):
	op = '->'
	def v(self, model, world):
		return not self.lchild.v(model, world) or self.rchild.v(model, world)
		
class Iff(BinOp):
	op = '<->'
	def v(self, model, world):
		return self.lchild.v(model, world) is self.rchild.v(model, world)
		
class UnOp(Formula):
	def __init__(self, child):
		self.child = child
	def __str__(self):
		return '(' + self.op + str(self.child) + ')'
		
class Not(UnOp):
	op = '~'
	def v(self, model, world):
		return not self.child.v(model, world)

class Box(UnOp):
	op = '[]'
	def v(self, model, world):
		nodes = []
		for i in range(len(model.nonAgentEdges)):
			if model.nonAgentEdges[i][0] == world:
				nodes.append(model.nonAgentEdges[i][1])
		#print "All worlds reachable from", world,": ", nodes
		return all(self.child.v(model, k) for k in nodes)
		
class Diamond(UnOp):
	op = '<>'
	def v(self, model, world):
		nodes = []
		for i in range(len(model.nonAgentEdges)):
			if model.nonAgentEdges[i][0] == world:
				nodes.append(model.nonAgentEdges[i][1])
		#print "All worlds reachable from", world,": ", nodes
		return any(self.child.v(model, k) for k in nodes)

class EpistemicOp(Formula):
	def __init__(self, agent, child):
		self.agent = agent
		self.child = child
	def __str__(self):
		return '(' + self.op + '_' + str(self.agent) + str(self.child) + ')'

class K(EpistemicOp):
	op = 'K'
	def v(self, model, world):
		nodes = []
		for i in range(len(model.edges[self.agent])):
			if model.edges[self.agent][i][0] == world:
				nodes.append(model.edges[self.agent][i][1])
		print "All worlds reachable from", world," by agent", self.agent, ": ", nodes
		return all(self.child.v(model, k) for k in nodes)
		
class M(EpistemicOp):
	op = 'M'
	def v(self, model, world):
		nodes = []
		for i in range(len(model.edges[self.agent])):
			if model.edges[self.agent][i][0] == world:
				nodes.append(model.edges[self.agent][i][1])
		print "All worlds reachable from", world," by agent", self.agent, ": ", nodes
		return any(self.child.v(model, k) for k in nodes)
		
class AnnounceOp(Formula):
	def __init__(self, formula, child):
		self.formula = formula
		self.child = child
	def __str__(self):
		return '(' + '(' + self.op + '_' + str(self.formula) + ')' + str(self.child) + ')'
		
class Announce(AnnounceOp):
	op = '[[]]'
	def v(self, model, world):
		nodesToDelete = []
		for key in model.nodes.keys():
			if self.formula.v(model, key) == False:
				nodesToDelete.append(key)
		for i in nodesToDelete:
			model.delNode(i)
		return self.child.v(model, world)
			
			
			
			
			
			
			
			
