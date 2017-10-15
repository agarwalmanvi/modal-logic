from model2 import *

m = Model()
m.addNodes(4)
m.addAgent('b')

ma = Atom('ma')
mb = Atom('mb')
m.addProp(0,ma)
m.addProp(0,mb)
m.addProp(1,ma)
m.addProp(2,mb)
m.addEdge(0,1,'b')
m.addEdge(2,3,'b')
m.addEdge(0,2,'a')
m.addEdge(1,3,'a')
m.transitiveClosure()
knoStr = KNS()
m.convertToKNS(knoStr)
