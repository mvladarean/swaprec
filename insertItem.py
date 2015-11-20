__author__ = 'Dih0r'

from systemParameters import *
from T1U2Exchange import *

#---------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------INSERTION-----------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

# TEST FOR INSERTION AND DELETION FROM ITEMLIST / WISHLIST AND ALGORITHM INVOCATION
#For the example held in the hardcodedData file if one new item I1 is inserted into u2’s wish
#list W2, the system first retrieves the users owning I1 in their unneeded item list
#Such users include u3 and u5. The system then
#tests if these candidate users have at least one critical item of u2.
#Since u5 does not contain any u2’s critical items {I6}, and u2 does
#not contain any u5’s critical items {I4, I6} in the unneeded item
#list. Therefore, u5 fails the test and u3 will be further checked by
#the 2-user item exchange algorithm.

def insertItem(updateUserId,
							 userBase,
							 wishlistOrItemlist,
							 ITEM_VALUES_TEST,
							 UL_TEST,
							 CL_TEST,
							 itemId,
							 itemValue = 0.0):
	if itemId not in ITEM_VALUES_TEST: # means that this item is new
		createDbEntriesForNewItem(itemId, itemValue, ITEM_VALUES_TEST, UL_TEST, CL_TEST)

	if wishlistOrItemlist == CHECK_WISHLIST:
		userBase[updateUserId].addItemToWishlist(itemId, userBase)

	elif wishlistOrItemlist == CHECK_ITEMLIST:
		userBase[updateUserId].addItemToItemlist(itemId, userBase)

	else:
		print("EEEEEEEEEEEERRRRRRRRROOOOOOOORRRRRRRRRR. Third parameter needs to be 0 or 1")


def createDbEntriesForNewItem(itemId,
															itemValue,
															ITEM_VALUES_TEST,
															UL_TEST,
															CL_TEST):
	# For new item we need to register it with the price
		ITEM_VALUES_TEST[itemID] = itemValue
		UL_TEST[itemId] = set()
		CL_TEST[itemId] = set()

'''
def generalTopKUpdate(updatedUser, userSet):
	usersWhoOwnMyCriticalItems = set()
	usersWhoWantCriticalItemsThatIOwn = set()

	for itemId in updatedUser.criticalItemList:
		usersWhoOwnMyCriticalItems |= set(UL_TEST[itemId])

	for itemId in updatedUser.unneededItemList:
		usersWhoWantCriticalItemsThatIOwn |= set(CL_TEST[itemId])

	for userId in usersWhoOwnMyCriticalItems & usersWhoWantCriticalItemsThatIOwn:
		#first two entries describe the gain for the updated user and the exchange tuple recommended for him
		(maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2) = T1U2Exchange(userSet[updatedUser.id], userSet[userId], EPSILON, BETA)

		#Update Top(k, i) and Top(k, l) accordingly
'''

