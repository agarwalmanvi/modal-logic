from agent import *
import copy
from copy import deepcopy
import numpy as np
import math
from itertools import chain, combinations
from graph_tool.all import *
from obsExp import *
from modalLogic import *
from expModel import *
from protExp import *

A = Agent('A')

class ProtModel:
	def __init__(self):
		self.TList = []
		self.Trel = dict()
		self.agentListProt = []
		self.agentListProt.append((A.name, A))
		self.Trel[self.agentListProt[0][0]] = np.zeros((1,1))
		self.prot = dict()
		
		self.Tnums = 0

		self.fcActions = []

	def __str__(self):
		return 'P'
		
	def addT(self):
		self.TList.append(self.Tnums)
		self.prot[self.Tnums] = ''
		if self.Tnums != 0:
			addBot = np.zeros((1,len(self.TList)-1))
			addSide = np.zeros((len(self.TList), 1))
			for i in self.Trel.keys():
				self.Trel[i] = np.concatenate((self.Trel[i],addBot), axis=0)
				self.Trel[i] = np.concatenate((self.Trel[i],addSide), axis=1)
		self.Tnums += 1
		
	def addTs(self, num):
		for t in range(num):
			self.addT()
		
	def addProt(self, t, protocol):
		if t in self.TList:
			self.prot[t] = protocol
			
	def addEdge(self, u, v, agent):
		if u in self.TList and v in self.TList:
			if type(agent) == str and agent in [i[0] for i in self.agentListProt]:
				indexU = self.TList.index(u)
				indexV = self.TList.index(v)
				self.Trel[agent][indexV][indexU] = 1
			elif agent.name in [i[0] for i in self.agentListProt]:
				indexU = self.TList.index(u)
				indexV = self.TList.index(v)
				self.Trel[agent.name][indexV][indexU] = 1

	def addAgent(self, agent):
		if type(agent) == str:
			self.agentListProt.append((agent,Agent(agent)))
			self.Trel[agent] = np.zeros((len(self.TList), len(self.TList)))
			matrix = self.Trel[agent]
		else:
			self.agentListProt.append((agent.name,agent))
			self.Trel[agent.name] = np.zeros((len(self.TList), len(self.TList)))
			matrix = self.Trel[agent.name]
			
	def addFC(self, fc):
		if type(fc) == list:
			self.fcActions = fc
		self.fcActions.append(fc)

















