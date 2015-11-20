__author__ = 'Dih0r'

import copy
from systemParameters import *
from T1U2Exchange import *


class ExchangeTuple:
	def __init__(self, giveToWhom, whatToGive, whatToReceive, gain):
		self.giveToWhom = giveToWhom
		self.whatToGive = whatToGive
		self.whatToReceive = whatToReceive
		self.gain = gain

	def toString(self):
		content = ""

		content += "(To: " + str(self.giveToWhom) + ", " \
						+ " give: " + str(self.whatToGive) + ", " \
						+ " receive: " + str(self.whatToReceive) + ", "\
						+ " gain: " + str(self.gain) + ")" + "\n"


		return content

class User:
	"""User class to retain useful information for each user registered in the system:

		Attributes:
				id: 							user unique identifier  (eg u1)
				unneededItemlist: set containing item ID for all items in the unneeded item list (eg i4)
				wishlist: 				set containing item ID for all items in the wishlist (eg i4)
				criticalItemList: set containing item ID for all items in teh cirtical list (eg i4)
				topK:							Dictionary keyed on the user to exchange with, containing pairs of sets
				 									(receive, give-away) tuples referring to the most lucrative relaxed_k exchanges for the user
				currentGain: 			the current value of the set that a user would get should the top exchange go through
	"""

	#TODO: fill the code with assertions!!!!!!!

	def __init__(self,
							 id,
							 unneededItemList,
							 wishList,
							 ITEM_VALUES_TEST,
							 UL_TEST,
							 CL_TEST,
							 WL_TEST,
							 RELATIVE_WORTH_TEST):
		self.id = id

		self.ITEM_VALUES_TEST = ITEM_VALUES_TEST
		self.UL_TEST = UL_TEST
		self.CL_TEST = CL_TEST
		self.WL_TEST = WL_TEST
		self.RELATIVE_WORTH_TEST = RELATIVE_WORTH_TEST

		self.unneededItemList = unneededItemList
		self.addHavesToTheInvertedLists()

		self.wishList = wishList
		self.addWishesToTheInvertedLists()

		self.currentGain = 0.0
		self.criticalItemList = set()
		self.computeCriticalItemList() #This also adds to the inverted list CL. Initially, the critical list will be all the wishlist, because the initial gain is not known

		self.topK = list()



	def deleteItemFromItemlist(self, itemId, userBase):
		self.unneededItemList.remove(itemId)

		self.updateInvertedListsRelatedToItemlist(itemId, OPERATION_DELETE)

		recompute = not(self.deleteTopkEntriesContainingItem(itemId, CHECK_GIVE_SET))

		if recompute == True:
			# recompute entire topk
			self.recomputeTopk(userBase)

		self.updateEveryoneForItemlistDelete(itemId, userBase)

	def updateEveryoneForItemlistDelete(self, itemId, userBase):
		for userID in self.WL_TEST[itemId]:
			foundIndex = userBase[userID].findUserInTopK(self.id)

			if foundIndex != -1 and \
				itemId in userBase[userID].topK[foundIndex].whatToReceive:

				needsRecomputation = not(userBase[userID].removeFromTopk(foundIndex))

				if needsRecomputation == True:
					userBase[userID].recomputeTopk(userBase)

	def deleteItemFromWishlist(self, itemId, userBase):
		self.wishList.remove(itemId)
		self.criticalItemList.remove(itemId)
		self.CL_TEST[itemId].remove(self.id)
		self.WL_TEST[itemId].remove(self.id)

		recompute = not(self.deleteTopkEntriesContainingItem(itemId, CHECK_GET_SET))

		if recompute == True:
			# recompute entire topk
			self.recomputeTopk(userBase)

		self.updateEveryoneForWishlistDelete(itemId, userBase)

	def updateEveryoneForWishlistDelete(self, itemId, userBase):
		for userId in self.UL_TEST[itemId]:
			foundIndex = userBase[userId].findUserInTopK(self.id)

			if foundIndex != -1 and\
				 itemId in userBase[userId].whatToGive:

				needToRecompute = not(userBase[userId].removeFromTopk(foundIndex))

				if needToRecompute:
					userBase[userId].recomputeTopk(userBase)

	def deleteTopkEntriesContainingItem(self, itemId, giveSetOrGetSet):
		idxToRemove = []

		# get deletion indexes
		if giveSetOrGetSet == CHECK_GIVE_SET:
			for idx, exchangeObject in enumerate(self.topK):
				if itemId in exchangeObject.whatToGive:
					idxToRemove.append(idx)

		elif giveSetOrGetSet == CHECK_GET_SET:
			for idx, exchangeObject in enumerate(self.topK):
				if itemId in exchangeObject.whatToReceive:
					idxToRemove.append(idx)

		# delete from topk
		if len(self.topK) - len(idxToRemove) >= HARD_K:
			i = 0
			for index in idxToRemove:
				self.topK.pop(index - i)
				i += 1

			#no need to sort because deleting items from list keeps the order, and the list was sorted before
			self.updateCurrentGainAndCriticalList(self.topK[0].gain)

			return True # this means removed, top K is ok

		else:
			return False # this means not removed, topK needs recomputation

	#---------------------------------------------------------------------------------------------------------------------
	#------------------------------------------INSERTION METHODS----------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------------------
	def addItemToWishlist(self, newItemId, userBase):

		self.wishList.add(newItemId)

		self.WL_TEST[newItemId].add(self.id)
		self.recomputeCriticalItemList()

		self.updateEveryoneForWishlistInsert(newItemId, userBase)

	def updateEveryoneForWishlistInsert(self, newItemId, userBase):

		# UL_TEST[itemId] users who own the new item
		for userId in self.UL_TEST[newItemId]:
			if self.criticalItemList & userBase[userId].unneededItemList:
				(maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2) = T1U2Exchange(userBase[self.id], userBase[userId], EPSILON, BETA, self.ITEM_VALUES_TEST)
				self.insertOrUpdateTopk(maxSwapU1_U2, gainUser1)

				if self.unneededItemList & userBase[userId].criticalItemList:
					userBase[userId].insertOrUpdateTopk(maxSwapU2_U1, gainUser2)

			elif self.unneededItemList & userBase[userId].criticalItemList:
				(maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2) = T1U2Exchange(userBase[self.id], userBase[userId], EPSILON, BETA, self.ITEM_VALUES_TEST)
				userBase[userId].insertOrUpdateTopk(maxSwapU2_U1, gainUser2)

	def addItemToItemlist(self, newItemId, userBase):
		self.unneededItemList.add(newItemId)

		self.updateInvertedListsRelatedToItemlist(newItemId, OPERATION_INSERT)

		self.updateEveryoneForItemlistInsert(newItemId, userBase)

	def updateEveryoneForItemlistInsert(self, newItemId, userBase):

		for userId in self.WL_TEST[newItemId]: # everybody who wants the newItem that I own
			if self.unneededItemList & userBase[userId].criticalItemList:
				(maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2) = T1U2Exchange(userBase[self.id], userBase[userId], EPSILON, BETA, self.ITEM_VALUES_TEST)
				userBase[userId].insertOrUpdateTopk(maxSwapU2_U1, gainUser2)

				if self.criticalItemList & userBase[userId].unneededItemList:
					self.insertOrUpdateTopk(maxSwapU1_U2, gainUser1)

			elif self.criticalItemList & userBase[userId].unneededItemList:
				(maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2) = T1U2Exchange(userBase[self.id], userBase[userId], EPSILON, BETA, self.ITEM_VALUES_TEST)
				userBase[userId].insertOrUpdateTopk(maxSwapU1_U2, gainUser1)

	#---------------------------------------------------------------------------------------------------------------------
	#------------------------------------------END INSERTION--------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------------------

	def findUserInTopK(self, userId):
		foundIndex = -1
		for idx, exchangeTuple in enumerate(self.topK):
			if userId == exchangeTuple.giveToWhom:
				foundIndex = idx
				break

		return foundIndex

	def insertOrUpdateTopk(self, newTuple, gainFromTuple):

		if newTuple == ():
			return

		assert isinstance(gainFromTuple, float), "New gain value is not a float: %r" % gainFromTuple
		assert self.id == newTuple[0], "ERROR: wrong tuple given for update. This does not belong to this user: %r" % newTuple[0]

		indexOfUser = self.findUserInTopK(newTuple[1])

		if indexOfUser != -1: # update user entry
			assert gainFromTuple >= self.topK[indexOfUser].gain, "ERROR: Trying to update a transaction to a worse value than before"

			self.topK[indexOfUser].whatToGive = copy.deepcopy(newTuple[3])
			self.topK[indexOfUser].whatToreceive = copy.deepcopy(newTuple[2])
			self.topK[indexOfUser].gain = gainFromTuple

		elif len(self.topK) < RELAXED_K:
			self.topK.append(ExchangeTuple(newTuple[1], newTuple[3], newTuple[2], gainFromTuple))

		else:
			if gainFromTuple > self.topK[len(self.topK) - 1].gain: # if bigger than min
				self.topK[len(self.topK) - 1] = ExchangeTuple(newTuple[1], newTuple[3], newTuple[2], gainFromTuple)

		self.topK.sort(key = lambda x: float(x.gain), reverse = True)

		self.updateCurrentGainAndCriticalList(self.topK[0].gain)

	def updateCurrentGainAndCriticalList(self, newVal):
		if newVal == self.currentGain:
			return

		assert isinstance(newVal, float), "New gain value is not a float: %r" % newVal

		self.currentGain = copy.copy(newVal)
		self.recomputeCriticalItemList()

	def recomputeTopk(self, userBase):
		self.updateCurrentGainAndCriticalList(0.0) # this makes the critical item list be identical to wishlist
		self.topK.clear()

		peopleOwningWhatIWant = set()
		for itemId in self.wishList:
			peopleOwningWhatIWant |= self.UL_TEST[itemId]

		for userId in peopleOwningWhatIWant:
			(maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2) = T1U2Exchange(userBase[self.id], userBase[userId], EPSILON, BETA, self.ITEM_VALUES_TEST)
			self.insertOrUpdateTopk(maxSwapU1_U2, gainUser1)

	def removeFromTopk(self, index):
		if len(self.topK) - 1 >= HARD_K:
			self.topK.pop(index)
			self.updateCurrentGainAndCriticalList(self.topK[0].gain)
			return True

		return False

	def computeCriticalItemList(self):
		assert len(self.criticalItemList) == 0, "ERROR: Critical list is not cleared!"

		totalWishlistValue = sum(float(self.ITEM_VALUES_TEST[itemID]) for itemID in self.wishList)
		sortedWishlistAccordingToRelativeWorth = sorted(self.wishList, key=lambda x: float(self.RELATIVE_WORTH_TEST[x]), reverse=True)
		#print("SORTED: " + str(sortRelativeValues))

		currentSum = 0.0
		index = 0
		#print("CriticalItemList in Recomputation: " + str(self.currentGain))
		while (totalWishlistValue - currentSum >= self.currentGain) and \
					(index < len(sortedWishlistAccordingToRelativeWorth)):

			currentSum += float(self.ITEM_VALUES_TEST[sortedWishlistAccordingToRelativeWorth[index]])
			self.criticalItemList.add(sortedWishlistAccordingToRelativeWorth[index])
			if sortedWishlistAccordingToRelativeWorth[index] in self.CL_TEST:
				self.CL_TEST[sortedWishlistAccordingToRelativeWorth[index]].add(self.id) #ADD THIS USER TO THE INVERTED LISTS FOR THE CORRESPONDING ITEMS
			else:
				self.CL_TEST[sortedWishlistAccordingToRelativeWorth[index]] = set(self.id)


			index += 1

	def recomputeCriticalItemList(self):
		previousCriticalItemList = copy.deepcopy(self.criticalItemList)

		self.criticalItemList.clear()
		self.computeCriticalItemList()

		# update inverted lists
		for itemId in previousCriticalItemList - self.criticalItemList:
			self.CL_TEST[itemId].remove(self.id)

		for itemId in self.criticalItemList - previousCriticalItemList:
			self.CL_TEST[itemId].add(self.id)

	def addHavesToTheInvertedLists(self):
		for itemId in self.unneededItemList:
			self.UL_TEST[itemId].add(self.id)

	def addWishesToTheInvertedLists(self):
		for itemId in self.wishList:
			self.WL_TEST[itemId].add(self.id)

	def updateInvertedListsRelatedToItemlist(self, updatedItemId, insertOrDelete):
		print()
		if insertOrDelete == OPERATION_INSERT:
			self.UL_TEST[updatedItemId].add(self.id)
		elif insertOrDelete == OPERATION_DELETE:
			self.UL_TEST[updatedItemId].remove(self.id)
		else:
			return

		if float(len(self.UL_TEST[updatedItemId])) != 0.0:
			self.RELATIVE_WORTH_TEST[updatedItemId] = float(self.ITEM_VALUES_TEST[updatedItemId]) / float(len(self.UL_TEST[updatedItemId]))
		else:
			self.RELATIVE_WORTH_TEST[updatedItemId] = float("-inf")

	def toString(self):
		user = ""

		topK = ""
		for item in self.topK:
			topK += item.toString()

		user += str(self.id) + " ------ " + " unneeded items: " + str(self.unneededItemList) + " \n" \
						+ " wish list: " + str(self.wishList) + " \n" \
						+ " critical item list: " + str(self.criticalItemList) + "\n" \
						+ " current gain: " + str(self.currentGain) + "\n" \
						+ " top K: " + topK + "\n"

		return user


