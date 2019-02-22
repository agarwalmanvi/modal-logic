from modalLogic import *
from pyparsing import Word, alphas, operatorPrecedence, Literal, oneOf, Suppress, nums, opAssoc, alphanums
from agent import *
import agent
from obsExp import *
from protExp import *

def getFormula(formula):
	if type(formula) == str:
		formula = [formula]
	if len(formula) == 1:
		return Atom(formula[0])

	f = formula[0]
	if f == "~":
		child = getFormula(formula[1])
		return Not(child)
	if f == "K":
		agent = Agent(formula[1])
		child = getFormula(formula[2])
		return K(agent, child)
	if f == "M":
		agent = Agent(formula[1])
		child = getFormula(formula[2])
		return M(agent, child)
	if f == "O":
		observation = obParser(formula[1])
		child = getFormula(formula[2])
		return O(observation, child)
	
	f = formula[1]
	if f == '->':
		a = getFormula(formula[0])
		b = getFormula(formula[2])
		return Imp(a,b)
	if f == "<->":
		a = getFormula(formula[0])
		b = getFormula(formula[2])
		return Iff(a,b)

	operands = []
	for token in formula:
		if token == f:
			continue
		child = getFormula(token)
		operands.append(child)

	if f == "|":
		expOr = Or(*operands)
		return expOr
	if f == "&":
		expAnd = And(*operands)
		return expAnd

def epParser(formulaString):
	operand = Word(alphanums, max=3)

	unaryOp = Literal('~')
	naryOp = oneOf('& |')
	binaryOp = oneOf('-> <->')
	epOp = oneOf('K M O')
	kOp = epOp + Suppress("(") + Word("("+alphanums+"."+"*"+"+"+")") + Suppress(",")

	expr = operatorPrecedence( operand,
	    [("~", 1, opAssoc.RIGHT),
	     (naryOp, 2, opAssoc.LEFT),
	     (binaryOp, 2, opAssoc.LEFT),
	     (kOp, 1, opAssoc.RIGHT)]
	    )

	ret = expr.parseString(formulaString)
	return getFormula(ret[0])

def getObFormula(formula):
	if type(formula) == str:
		formula = [formula]
	if len(formula) == 1:
		if formula[0] == "delta":
			return DeltaObs()
		if formula[0] == "eps":
			return EpsilonObs()
		return AlphabetObs(formula[0])
	
	f = formula[1]
	operands = []
	for token in formula:
		if token == f:
			continue
		child = getObFormula(token)
		operands.append(child)

	if f == ".":
		expDot = DotObs(*operands)
		return expDot
	if f == "+":
		expPlus = PlusObs(*operands)
		return expPlus


def obParser(formulaString):
	operand = Word(alphanums)
	naryOp = oneOf('+ .')

	expr = operatorPrecedence( operand, [(naryOp, 2, opAssoc.LEFT)])

	ret = expr.parseString(formulaString)
	print('Here we have a ret: ', ret)
	return getObFormula(ret[0])

def getProtFormula(formula):
	print('first form of formula: ', formula)
	if type(formula) == str:
		formula = [formula]
		print('1. formula: ', formula)
	if len(formula) == 1:
		if formula[0] == "d":
			print('2. returning delta: ', formula[0])
			return DeltaProt()
		if formula[0] == "e":
			print('3. returning epsilon: ', formula[0])
			return EpsilonObs()
		print('3. returning alphabet: ', formula[0])
		return AlphabetProt(formula[0])
		
	f = formula[0]
	if f == "?":
		child = epParser(formula[1])
		print('This is the child: ', child)
		return AskProt(child)
	
	f = formula[1]
	print('4. here is f: ', f)
	operands = []
	for token in formula:
		print('This is a token: ',token)
		if token == f:
			continue
		child = getProtFormula(token)
		operands.append(child)
	print('5. here are the operands: ', operands)

	if f == ".":
		expDotProt = DotProt(*operands)
		print('we are returning a dotprot object!')
		return expDotProt
	if f == "+":
		expPlusProt = PlusProt(*operands)
		print('we are returning a plusprot object!')
		return expPlusProt

def protParser(formulaString):
	operand = Word(alphanums)

	unaryOpProt = Literal('?')
	naryOpProt = oneOf('+ .')
	
	expr = operatorPrecedence( operand,
	    [(unaryOpProt, 1, opAssoc.RIGHT),
	     (naryOpProt, 2, opAssoc.LEFT),]
	    )
	
	ret = expr.parseString(formulaString)
	print("Here is ret: ",ret)
	#TODO run sample to see why the expr is getting shortened here
	return getProtFormula(ret[0])



