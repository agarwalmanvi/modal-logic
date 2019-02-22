class Agent:
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return str(self.name)
	def __hash__(self):
		return hash(self.name)

