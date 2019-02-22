from agent import *
from copy import deepcopy
import numpy as np
import math
from itertools import chain, combinations
from graph_tool.all import *
from obsExp import *
from modalLogic import *
from protModel import *

A = Agent('A')

class Model:
	def __init__(self):
		self.nodeList = []
		self.val = dict()
		self.worldsNum = 0
		self.propList = []
		self.agentList = []
		self.agentList.append((A.name, A))
		self.rel = dict()
		self.rel[self.agentList[0][0]] = np.zeros((1,1))
		
		self.nodesRef = dict()
		
		self.expectations = dict()
		
		self.g = Graph()
		
		self.fcActions = []
		
	def clearModel(self):
		self.nodeList = []
		self.val = dict()
		self.worldsNum = 0
		self.rel = dict()
		self.rel[self.agentList[0][0]] = np.zeros((1,1))
		
		self.expectations = dict()
		
		self.nodesRef = dict()
		
		self.g = Graph()

	def addNode(self):
		self.nodeList.append(self.worldsNum)
		self.val[self.worldsNum] = []
		self.expectations[self.worldsNum] = 0		
		if self.worldsNum != 0:
			addBot = np.zeros((1,len(self.nodeList)-1))
			addSide = np.zeros((len(self.nodeList), 1))
			for i in self.rel.keys():
				self.rel[i] = np.concatenate((self.rel[i],addBot), axis=0)
				self.rel[i] = np.concatenate((self.rel[i],addSide), axis=1)
		self.worldsNum = self.worldsNum + 1

	def addNodes(self, num):
		for i in range(num):
			self.addNode()
			
	def addAgent(self, agent):
		if type(agent) == str:
			self.agentList.append((agent,Agent(agent)))
			self.rel[agent] = np.zeros((len(self.nodeList), len(self.nodeList)))
			matrix = self.rel[agent]
		else:
			self.agentList.append((agent.name,agent))
			self.rel[agent.name] = np.zeros((len(self.nodeList), len(self.nodeList)))
			matrix = self.rel[agent.name]
			
	def deleteNode(self, node):
		if node in self.nodeList:
			index = self.nodeList.index(node)
			for i in self.rel.keys():
				self.rel[i] = np.delete(self.rel[i], (index), axis=0)
				self.rel[i] = np.delete(self.rel[i], (index), axis=1)
			self.nodeList.remove(node)
			del self.val[node]
			del self.expectations[node]
			
	def addEdge(self, u, v, agent):
		if u in self.nodeList and v in self.nodeList:
			if type(agent) == str and agent in [i[0] for i in self.agentList]:
				indexU = self.nodeList.index(u)
				indexV = self.nodeList.index(v)
				self.rel[agent][indexV][indexU] = 1
			elif agent.name in [i[0] for i in self.agentList]:
				indexU = self.nodeList.index(u)
				indexV = self.nodeList.index(v)
				self.rel[agent.name][indexV][indexU] = 1

	def addProp(self, node, prop):
		if type(prop) == Atom:
			if node in self.nodeList:
				self.val[node].append(prop)
			if prop not in self.propList:
				self.propList.append(prop)
		
		
	def addPropToAll(self, prop):
		if type(prop) == Atom:
			for i in self.nodeList:
				self.addProp(i, prop)

	def transitiveClosure(self):
		for agent in [i[0] for i in self.agentList]:
			for k in range(len(self.nodeList)):
				for i in range(len(self.nodeList)):
		         		for j in range(len(self.nodeList)):
		         			self.rel[agent][i][j] = self.rel[agent][i][j] or (self.rel[agent][i][k] and self.rel[agent][k][j])

	#define \sigma of alphabets for regex
#	def buildLang(self, *argv):
#		for arg in argv:
#			self.sigma.append(arg)

	def addObservation(self, node, obs):
		self.expectations[node] = obs
		
	def addFC(self, fc):
		if type(fc) == list:
			self.fcActions = fc
		self.fcActions.append(fc)
		
	

	def v(self, formula, world):
		if type(formula) == Atom:
			return formula in self.val[world]
		elif type(formula) == Not:
			return not self.v(formula.child,world)
		elif type(formula) == Or:
			return any(self.v(child, world) for child in formula.children)
		elif type(formula) == And:
			return all(self.v(child, world) for child in formula.children)
		elif type(formula) == Imp:
			return not self.v(formula.leftChild,world) or self.v(formula.rightChild,world)
		elif type(formula) == Iff:
			return self.v(formula.leftChild,world) is self.v(formula.rightChild,world)
		elif type(formula) == modalLogic.K:
			nodes = []
			for i in range(len(self.nodeList)):
				if self.rel[formula.agent.name][self.nodeList.index(world)][i] == 1:
					nodes.append(self.nodeList[i])
			return all(self.v(formula.child, k) for k in nodes)
		elif type(formula) == modalLogic.M:
			nodes = []
			for i in range(len(self.nodeList)):
				if self.rel[formula.agent.name][self.nodeList.index(world)][i] == 1:
					nodes.append(self.nodeList[i])
			return any(self.v(formula.child, k) for k in nodes)
		elif type(formula) == O:
			self.updateModel(formula.observation)
			if world in self.nodeList:
				return self.v(formula.child, world)
			else:
				return True
		elif type(formula) == P:
			self.installProtocol(formula.protocol)
			#TODO finish this
		
		
	def updateModel(self, expression):
		delList = []
		for i in self.nodeList:
			self.expectations[i] = makeObservation(self.expectations[i],expression)
			if type(self.expectations[i]) == DeltaObs:
				delList.append(i)
			else:
				continue
		for node in delList:
			self.deleteNode(node)
		
	def installProtocol(self, protModel):
		tempNodeList = self.nodeList
		tempVal = self.val
		temprel = self.rel
		self.clearModel()
		counter = 0
		for node in tempNodeList:
			for t in protModel.TList:
				if type((protModel.prot[t]).f(tempVal[node])) != DeltaObs:
					self.addNode()
					self.nodesRef[self.worldsNum-1] = (node,t)
					self.val[self.worldsNum-1] = tempVal[node]
					self.expectations[self.worldsNum-1] = simplify(protModel.prot[t].f(tempVal[node]))
		for agent in [i[0] for i in self.agentList]:
			if agent not in self.rel.keys():
					self.rel[agent] = np.zeros((len(self.nodeList), len(self.nodeList)))
			for u in self.nodesRef.keys():
				for v in self.nodesRef.keys():
					nodeU = self.nodesRef[u]
					nodeV = self.nodesRef[v]
					if temprel[agent][nodeU[0]][nodeV[0]] == 1 and protModel.Trel[agent][nodeU[1]][nodeV[1]] == 1:
						self.rel[agent][u][v] = 1
		self.fcActions = protModel.fcActions



	def draw(self, fileName):
		graphNode = dict()	#graphNode is a dict with node number for keys and Vertex object for values
		for i in self.nodeList:	
			graphNode[i] = self.g.add_vertex()
		edgeList = []		#edgeList is the minimal edge list without any agent references --- does not contain reflexive edges, and only represents those edges which convey the link between any two different nodes
		drawAgentList = []
		for nodeU in range(len(self.nodeList)):
			for nodeV in range(len(self.nodeList)):
				for agent in [i[0] for i in self.agentList]:
					if self.rel[agent][nodeU][nodeV] == 1 and (nodeU, nodeV) not in edgeList:
							edgeList.append((nodeU,nodeV))
		edges = dict()		#edges is a dict with elements of edgeList for keys and the agents on that edge for values
		for i in edgeList:
			self.g.add_edge(graphNode[i[0]],graphNode[i[1]])
			edges[i] = []
			for agent in [i[0] for i in self.agentList]:
				if self.rel[agent][i[0]][i[1]] == 1 :
					edges[i].append(agent)
		#Generate edge property for relation
		edgeAgents = self.g.new_edge_property("string")
		for i in edgeList:
			source = i[0]
			target = i[1]
			edgeAgents[self.g.edge(source, target)] = ', '.join(edges[i])
		self.g.edge_properties["edgeAgent"] = edgeAgents
		target = "./public/imgs/" + str(fileName) + ".png"
		#x, y = ungroup_vector_property(pos, [0, 1])
		#x.a = (x.a - x.a.min()) / (x.a.max() - x.a.min()) * 200 + 100
		#y.a = (y.a - y.a.min()) / (y.a.max() - y.a.min()) * 200 + 100
		#pos = group_vector_property([x, y])
		#TODO the images are getting cut off, change it to show the full graph!
		graph_draw(self.g, vertex_text=self.g.vertex_index, edge_text=self.g.edge_properties["edgeAgent"], vertex_font_size=18, edge_font_size=25, edge_pen_width=2.75, edge_text_distance=8.5, output_size=(1000, 1000), output=target)
		






#########################################################EXTERNAL FUNCTIONS################################################################
	


































