class neural:
	def __init__(self, N):
		self.weights = list()
		for i in range(N):
			self.weights.append(0)
	def getNumber(self, x):
		result =  0
		for i in range(len(self.weights)):
			result = result + self.weights[i] * x[i]
		return result
	def sign(self, x):
		if self.getNumber(x) > 1:
			return 1
		else:
			return 0
	def study(self, la, x, y):
		if y * self.getNumber(x) <=  0:
			for i in range(len(self.weights)):
				self.weights[i] = self.weights[i] + la * y * x[i]
	def learning(self, la, T):
		for n in range(1000 * len(T)):
			for t in T:
				self.study(la, t[0], t[1])