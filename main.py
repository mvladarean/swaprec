__author__ = 'Dih0r'

from DataFlowController import *

if DATA_FLOW_CONTROLLER == BOOKMOOCH_DATA_FLAG:
	from bookmoochData import *
else:
	from hardcodedData import *

import User
from T1U2Exchange import *
from insertItem import *
from deleteItem import *
from systemParameters import *


'''

itemset = set(["i1", "i2", "i3"])

avt = dict()
avt = AVT.AVT(1, 0.5, itemset)
print(avt.toString())
'''
# GENERATE USERS AND THEIR CRITICAL SETS

# CREATE USER SET
USERS = dict()
for userId, wishlist in WISHLISTS_TEST.items():
	wishList = set(wishlist)
	unneededItemList = set(ITEMLISTS_TEST[userId])

	USERS[userId] = User.User(userId,
														unneededItemList,
														wishList,
														ITEM_VALUES_TEST,
														UL_TEST,
							 							CL_TEST,
							 							WL_TEST,
							 							RELATIVE_WORTH_TEST)
	# This part also fills the inverted lists UL_TEST and CL_TEST


# COMPUTE TOP 2 FOR EACH AT THIS INITIAL STEP => WILL UPDATE THE CRITICAL LISTS
for userId1, userObject1 in sorted(USERS.items(), key=lambda x: x[0]):
	for userId2, userObject2 in sorted(USERS.items(), key=lambda x: x[0]):

		if userId1 >= userId2:
			continue


		(maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2) = T1U2Exchange(userObject1, userObject2, EPSILON, BETA, ITEM_VALUES_TEST)

		if (gainUser1 == 0.0 and gainUser2 == 0.0):
			#print("+++++++ " + str(userObject1.id) + " - " + str(userObject2.id) + ": No viable exchange")
			print()
		else:
			userObject1.insertOrUpdateTopk(maxSwapU1_U2, gainUser1)
			userObject2.insertOrUpdateTopk(maxSwapU2_U1, gainUser2)

			#print("+++++++ " + str(userObject1.id) + " - " + str(userObject2.id) + " SWAP:" + \
			#			userId1 + " - Recommendation: " + str(maxSwapU1_U2) + ", gain = " + str(gainUser1) + ", " + str(userId2) + \
			#			" - Recommendation: " + str(maxSwapU2_U1) + ", gain = " + str(gainUser2))

print("================================================================================================================")
print("==================================================INITIALLY=====================================================")
print("================================================================================================================")


for userId1, userObject1 in sorted(USERS.items(), key=lambda x: x[0]):
	print(userObject1.toString())
	print("\n-----------------------------------------------\n")


# AT THIS POINT WE HAVE THE INITIAL RECOMMENDATIONS.
#TODO: Write code for when a user is inserted into the system as well

print("================================================================================================================")
print("============================AFTER INSERTION OF i3 in u1 wishlist================================================")
print("================================================================================================================")

insertItem("u1", USERS, CHECK_WISHLIST, ITEM_VALUES_TEST, UL_TEST, CL_TEST, "i3")

for userId1, userObject1 in sorted(USERS.items(), key=lambda x: x[0]):
	print(userObject1.toString())
	print("\n-----------------------------------------------\n")


print("================================================================================================================")
print("============================AFTER DELETION OF i5 in u2 have list================================================")
print("================================================================================================================")

deleteItem("u2", USERS, CHECK_ITEMLIST, "i5", ITEM_VALUES_TEST)

for userId1, userObject1 in sorted(USERS.items(), key=lambda x: x[0]):
	print(userObject1.toString())
	print("\n-----------------------------------------------\n")
