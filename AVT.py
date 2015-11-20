__author__ = 'Dih0r'
'''
from DataFlowController import *

if DATA_FLOW_CONTROLLER == BOOKMOOCH_DATA_FLAG:
	from bookmoochData import *
else:
	from hardcodedData import *
'''
import copy
import math
import ApproximateValue

class AVT:
	"""Approximate value table to hold the information about the approximate value classes of all the subsets of a input
		 set of items. The inputted sets given by the algorithm will be the results of one the following intersections:
		 		* W_i with L_j
		 		* W_j with L_i

		Attributes:
				epsilon: parameter denoting the error tolerance, i.e. the gain computed with this approximate method will be
								 no worse than (1 - epsilon) * OptimalGain
				beta:		 relaxation parameter in the interval (0, 1] such that the sets recommended for exchange, S1, S2,
								 satisfy the property beta * S1 <= S2 <= 1/beta * S1
				itemset: set containing item IDs.
				vmin: 	 the minimal value of any non-empty item combination from the set "itemset"
				N: 			 the maximal number of items
				table: 	 the approximate value table resulting from the computation
	"""

	def __init__(self, epsilon, beta, itemset, ITEM_VALUES_TEST):
		self.epsilon = epsilon
		self.beta = beta
		self.itemset = itemset
		self.ITEM_VALUES_TEST = ITEM_VALUES_TEST
		self.vmin = self.retrieveVmin()
		self.N = len(itemset)
		self.table = dict()

		self.createAVTTable()

	#---------------------------------------------------------------------------------------------------------------------
	#-----------------------------------------------ALGORITHM 3 FCS-------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------------------

	def initializeTable(self):
		self.table.clear() #just to be sure
		#self.table[0] = ApproximateValue.ApproximateValue()


	def createAVTTable(self):
		self.initializeTable()

		for itemID in sorted(self.itemset):
			#print("----------------------------Item " + str(itemID) + "---------------------------\n\n")
			self.updateAVT(itemID)
			#print(self.toString())


	def updateAVT(self, itemID):
		newAVTEntries = dict()

		itemValue = self.ITEM_VALUES_TEST[itemID]

		#print(str(sorted(self.table.items(), key=lambda x: int(x[0]))))

		# -------------------------------Attempt item insertion by itself, against category with value 0--------------------
		newValueCategory = self.computeValueCategory(float(self.ITEM_VALUES_TEST[itemID]))
		if newValueCategory in self.table:
			self.updateEntry(self.table, newValueCategory, "none", ApproximateValue.ApproximateValue(), itemID, itemValue)
		elif newValueCategory in newAVTEntries:
			self.updateEntry(newAVTEntries, newValueCategory, "none", ApproximateValue.ApproximateValue(), itemID, itemValue)
		else:
			self.addEntry(newAVTEntries, newValueCategory, "none", ApproximateValue.ApproximateValue(), itemID, itemValue)
		# -------------------------------END Attempt item insertion by itself-----------------------------------------------

		for valueCategory, approximateValueObject in sorted(self.table.items(), key=lambda x: int(x[0])):
			newValueCategory = self.computeValueCategory(float(approximateValueObject.value) + float(itemValue))

			if newValueCategory in self.table:
				self.updateEntry(self.table, newValueCategory, valueCategory, approximateValueObject, itemID, itemValue)

			elif newValueCategory in newAVTEntries:
				self.updateEntry(newAVTEntries, newValueCategory, valueCategory, approximateValueObject, itemID, itemValue)

			else:
				self.addEntry(newAVTEntries, newValueCategory, valueCategory, approximateValueObject, itemID, itemValue)

		# The objects in newAVTEntries are not checked against item because they themselves were created by using the item
		self.table.update(newAVTEntries)

	def updateEntry(self,
									avtDictionary,
									keyToBeUpdated,
									currentKey,
									currentApproxValObject,
									incomingItemId,
									incomingItemValue):
		#print("UPDATE")
		newApproximateValueEntry = copy.deepcopy(avtDictionary[keyToBeUpdated]) #get previous version

		if (currentApproxValObject.lb + incomingItemValue < avtDictionary[keyToBeUpdated].lb) and \
			  not(incomingItemId in currentApproxValObject.lbi):

			newApproximateValueEntry.lb  = currentApproxValObject.lb + incomingItemValue
			newApproximateValueEntry.lbi = copy.deepcopy(currentApproxValObject.lbi)
			newApproximateValueEntry.lbi.add(incomingItemId)

		if (currentApproxValObject.ub + incomingItemValue > avtDictionary[keyToBeUpdated].ub) and \
				not(incomingItemId in currentApproxValObject.ubi):

			newApproximateValueEntry.ub = currentApproxValObject.ub + incomingItemValue
			newApproximateValueEntry.ubi = copy.deepcopy(currentApproxValObject.ubi)
			newApproximateValueEntry.ubi.add(incomingItemId)

		#print("Previous: " + currentApproxValObject.toString() + " key: " + str(currentKey))
		#print("updated: " + newApproximateValueEntry.toString() + " at key: " + str(keyToBeUpdated) + "\n\n\n")

		avtDictionary[keyToBeUpdated] = newApproximateValueEntry


	def addEntry(self,
							 avtDictionary,
							 keyToBeUpdated,
							 currentKey,
							 currentApproxValObject,
							 incomingItemId,
							 incomingItemValue):

		#print("ADD")
		lowerBoundSet = copy.deepcopy(currentApproxValObject.lbi)
		lowerBoundSet.add(incomingItemId)

		upperBoundSet = copy.deepcopy(currentApproxValObject.ubi)
		upperBoundSet.add(incomingItemId)

		newApproximateValue = self.vmin * (1 - self.epsilon / float(self.N)) ** (-keyToBeUpdated) #2.0 ** keyToBeUpdated

		newApproximateValueEntry = ApproximateValue.ApproximateValue(currentApproxValObject.lb + incomingItemValue,
																																 currentApproxValObject.ub + incomingItemValue,
																																 lowerBoundSet,
																																 upperBoundSet,
																																 newApproximateValue)
		#print("Previous: " + currentApproxValObject.toString() + " key: " + str(currentKey))
		#print("ADDED: " + newApproximateValueEntry.toString() + " at key: " + str(keyToBeUpdated) + "\n\n\n")
		avtDictionary[keyToBeUpdated] = newApproximateValueEntry


	#---------------------------------------------------------------------------------------------------------------------
	#-------------------------------------------------HELPER FCS----------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------------------

	def retrieveVmin(self):
		minVal = min(self.ITEM_VALUES_TEST.values())

		return minVal


	def computeValueCategory(self, value):
		numerator = math.log(self.vmin) - math.log(value)
		denominator = math.log(1.0 - float(self.epsilon) / float(self.N)) #- math.log(2.0)

		return math.ceil(numerator / denominator)


	def toString(self):
		avt = ""

		for valueKey, approximateValueObject in self.table.items():
			avt += str(valueKey) + " ------ " + approximateValueObject.toString() + "\n"

		return avt