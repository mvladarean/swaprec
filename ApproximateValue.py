__author__ = 'Dih0r'

class ApproximateValue:
	"""Approximate value object which retains class characteristics:

		Attributes:
				lb: a real number denoting the lower bound value of the sets of items in this object
				ub: a real number denoting the upper bound value of the sets of items in this object
				lbi: the set of items reaching the lower bound lb
				ubi: the set of items reaching the upper bound ub
				value: the approximate value of the items in this class computed as vmin*(1 - epsilon/N)^(-m)
	"""

	def __init__(self,
							 lb=0.0,
							 ub=0.0,
							 lbi=set(),
							 ubi=set(),
							 value=0.0):

		self.lb = lb
		self.ub = ub
		self.lbi = lbi
		self.ubi = ubi
		self.value = value


	def toString(self):
		return "Lower bound: " + str(self.lb) + ", " \
					 + "Lower bound set: " + str(self.lbi) + ", " \
					 + "Upper bound: " + str(self.ub) + ", " \
					 + "Upper bound set: " + str(self.ubi) + ", " \
					 + "Approximate value: " + str(self.value)
