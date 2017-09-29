from modal import *
from copy import deepcopy

class Model:
	def __init__(self):
		self.nodes = dict()
		self.edges = dict()
		self.nonAgentEdges = []
		self.worldsNum = 0
		self.agents = []
		self.type = 'S5' #Can be changed to 'K': this simply influences how you add edges, S5 adds edges wrt ref, sy, trans/K adds 						edges individually
	
	def addAgent(self, agent):
		if agent not in self.agents:
			self.agents.append(agent)
			self.edges[agent] = []
			if self.nodes:
				for key in self.nodes.keys():
					self.edges[agent].append((key, key))
		else:
			print "That agent already exists!"
	
	def addNode(self):
		self.nodes[self.worldsNum] = []
		#When you create a world you it is automatically reflexive for all agents if type is S5
		if self.type == 'S5':
			for i in self.agents:
				self.edges[agent].append((self.worldsNum, self.worldsNum))
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
	def addEdge(self, w1, w2, agent):
		if self.type == 'K':
			if (w1,w2) not in self.edges[agent]:
				if w1<self.worldsNum and w2<self.worldsNum and agent in self.agents:
					self.edges[agent].append((w1,w2))
					if (w1, w2) not in self.nonAgentEdges:
						self.nonAgentEdges.append((w1,w2))
				else:
					print "Sorry; those agent/world(s) don't exist!"
			else:
				print "This edge already exists."
		else:
			if (w1,w2) not in self.edges[agent]:
				if w1<self.worldsNum and w2<self.worldsNum and agent in self.agents:
					self.edges[agent].append((w1,w2))			#
					if (w1, w2) not in self.nonAgentEdges:			#
						self.nonAgentEdges.append((w1,w2))		#		
					self.edges[agent].append((w2,w1))			# SYMMETRIC
					if (w2, w1) not in self.nonAgentEdges:			#
						self.nonAgentEdges.append((w2,w1))		#	
					for key in self.nodes.keys():
						if (key,w1) in self.edges[agent] and (w1,w2) in self.edges[agent]:
							if (key,w2) not in self.edges[agent]:			#
								self.edges[agent].append((key,w2))		#
							if (key, w2) not in self.nonAgentEdges:			#
								self.nonAgentEdges.append((key,w2))		# TRANSITIVE
							if (w2,key) not in self.edges[agent]:			#	
								self.edges[agent].append((w2,key))		#
							if (w2, key) not in self.nonAgentEdges:			#
								self.nonAgentEdges.append((w2,key))
						if (w2,w1) in self.edges[agent] and (w1,key) in self.edges[agent]:
							if (w2,key) not in self.edges[agent]:
								self.edges[agent].append((w2,key))
							if (w2, key) not in self.nonAgentEdges:
								self.nonAgentEdges.append((w2,key))
							if (key,w2) not in self.edges[agent]:
								self.edges[agent].append((key,w2))
							if (key, w2) not in self.nonAgentEdges:
								self.nonAgentEdges.append((key,w2))
				else:
					print "Sorry; those agent/world(s) doesn't/don't exist!"
			else:
				print "This edge already exists."

	def delNode(self, node):
		if node in self.nodes:
			del self.nodes[node]
			copyEdges = dict()
			for i in self.agents:
				copyEdges[i] = []
			for i in self.agents:
				for j in self.edges[i]:
					if j[0] != node and j[1] != node:
						copyEdges[i].append(j)
			self.edges = deepcopy(copyEdges)
			copyNonAgentEdges = []
			for i in self.nonAgentEdges:
				if i[0] != node and i[1] != node:
					copyNonAgentEdges.append(i)
			self.nonAgentEdges = deepcopy(copyNonAgentEdges)
		else:
			print "That node doesn't exist!"
					









"""		
	def draw(self):
		g = Graph()
		valuation = g.new_vertex_property("vector<int>")
		for i in range(self.worldsNum):
			g.add_vertex()
			valuation(g.vertex(i)) = m.nodes[i]
"""
		














