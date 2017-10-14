from model2 import *

m = Model()
m.addNodes(4)
m.addAgent('b')
m.addEdge(0,1,'a')
m.addEdge(1,2,'a')
m.addEdge(0,2,'b')
m.addEdge(1,3,'b')
m.transitiveClosure()
"""
p = Atom('p')
q = Atom('q')
m.addProp(0,p)
m.addProp(1,q)
"""
