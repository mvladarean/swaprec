__author__ = 'Dih0r'


class AVTMinValError(Exception):
	def __init__(self, value):
		self.value = "The min value of any non empty item set should be positive"\
								 "The current min value is: " + str(value)

	def __str__(self):
		return repr(self.value)


