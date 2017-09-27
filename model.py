from mylogic import *

class Model:
	def __init__(self):
		#dict recording which propositional atoms are true in which worlds
		self.nodes = dict()
		self.edges = []
		self.worldsNum = 0
		self.agents = []
	
	def addNode(self):
		self.nodes[self.worldsNum] = []
		self.worldsNum = self.worldsNum + 1
		
	def addNodes(self, num):
		for i in range(self.worldsNum, num):
			self.addNode()
			
	def addProp(self, prop, node):
		self.nodes[node].append(prop)
		
	def addPropToAll(self, prop):
		for i in range(0, self.worldsNum):
			self.nodes[i].append(prop)
			
	#add edges individually
	def addEdge(self, w1, w2):
		if (w1,w2) not in self.edges:
			if w1<self.worldsNum and w2<self.worldsNum:
				self.edges.append((w1,w2))
			else:
				print "Sorry; those world(s) don't exist!"
		else:
			print "This edge already exists."
			
	#For propositional formulas
	def evaluate(self, formula, node):
		return formula.v(self.nodes[node])
