from modal2 import *
from copy import deepcopy
import numpy as np
import math

class Model:
	def __init__(self):
		self.nodeList = []
		self.mat = np.zeros((1,1))
		self.val = dict()
		self.worldsNum = 0
		
		self.agentList = ['a']
		self.rel = dict()
		self.rel[self.agentList[0]] = np.zeros((1,1))
		
		"""
		self.matrix = np.zeros((4,4))
		for i in range(4):
			self.matrix[i][i] = 1
		self.matrix[0][3] = 1
		self.matrix[3][0] = 1
		self.nodeList = [0,1,2,3]
		"""
		self.visited = []
		self.parts = dict()
		self.onePart = []
		self.l = []
		self.obs = dict()
		
	def addNode(self):
		self.nodeList.append(self.worldsNum)
		self.val[self.worldsNum] = []
		if self.worldsNum == 0:
			for i in self.rel.keys():
				self.rel[i][0][0] = 1
				self.val[0] = []
		else:
			addBot = np.zeros((1,self.worldsNum))
			addSide = np.zeros((1,self.worldsNum+1)).T
			for i in self.rel.keys():
				self.rel[i] = np.concatenate((self.rel[i],addBot), axis=0)
				self.rel[i] = np.concatenate((self.rel[i],addSide), axis=1)
				self.rel[i][self.worldsNum][self.worldsNum] = 1
			self.val[self.worldsNum] = []
		self.worldsNum = self.worldsNum + 1
		
	def addNodes(self, num):
		for i in range(num):
			self.addNode()
			
	def addAgent(self, agent):
		self.agentList.append(agent)
		nodes = len(self.nodeList)
		self.rel[agent] = np.zeros((nodes, nodes))
		matrix = self.rel[agent]
		for i in range(nodes):
			matrix[i][i] = 1
			
	def deleteNode(self, node):
		if node in self.nodeList:
			index = self.nodeList.index(node)
			for i in self.rel.keys():
				self.rel[i] = np.delete(self.rel[i], (index), axis=0)
				self.rel[i] = np.delete(self.rel[i], (index), axis=1)
			self.nodeList.remove(node)
			del self.val[node]
		else:
			print "That node doesn't exist!"
			
	def addEdge(self, u, v, agent):
		if u in self.nodeList and v in self.nodeList and agent in self.agentList:
			indexU = self.nodeList.index(u)
			indexV = self.nodeList.index(v)
			self.rel[agent][indexV][indexU] = 1
			self.rel[agent][indexU][indexV] = 1
	
	def transitiveClosure(self):
		for agent in self.agentList:
			for k in range(len(self.nodeList)):
				for i in range(len(self.nodeList)):
		         		for j in range(len(self.nodeList)):
						self.rel[agent][i][j] = self.rel[agent][i][j] or (self.rel[agent][i][k] and self.rel[agent][k][j])
					
	def addProp(self, node, prop):
		if node in self.nodeList:
			self.val[node].append(prop)
		
	def addPropToAll(self, prop):
		for i in self.nodeList:
			self.addProp(i, prop)
			
	def convertToKNS(self):
		self.findConnected()
		print self.parts
		self.l = [0]*len(self.agentList)
		for i in self.parts.keys():
			self.l[self.agentList.index(i)] = math.ceil(math.log(len(self.parts[i]),2))
		for agent in self.agentList:
			self.obs[agent] = []
		
	
	def findConnected(self):	
		for agent in self.agentList:
			self.parts[agent] = []
			self.matrix = self.rel[agent]
			self.visited = [0]*len(self.nodeList)
			for i in self.nodeList:
				self.onePart = []
				if self.visited[self.nodeList.index(i)] == 0:
					self.DFSUtil(i)
				if self.onePart:
					self.parts[agent].append(self.onePart)
				
	def DFSUtil(self, node):
		self.visited[self.nodeList.index(node)] = 1
		self.onePart.append(node)
		for j in self.nodeList:
			if self.matrix[self.nodeList.index(node)][self.nodeList.index(j)] == 1:
				if self.visited[self.nodeList.index(j)] == 0:
					self.DFSUtil(j)
		
class KNS:
	def __init__(self):
		self.V = []
		self.obs = dict()
		self.stateLaw = 'This stays empty for now'
		
	
	
