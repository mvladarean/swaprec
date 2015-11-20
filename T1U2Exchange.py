__author__ = 'Dih0r'
import AVT


#---------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------T1U2Exchange-------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

# ALGORITHM 3
# works well!
def T1U2Exchange(user1,
								 user2,
								 epsilon,
								 beta,
								 ITEM_VALUES_TEST):

	W1_I2 = user1.wishList & user2.unneededItemList
	W2_I1 = user2.wishList & user1.unneededItemList

	gainUser1 = 0.0
	gainUser2 = 0.0
	maxSwapU1_U2 = ()
	maxSwapU2_U1 = ()

	if len(W1_I2) != 0 and len(W2_I1) != 0:
		#print("\n\n--------------------------------AVT TABLES FOR " + str(user1.id) + ", " + str(user2.id) + "----------------")
		AVT1 = AVT.AVT(epsilon, beta, W1_I2, ITEM_VALUES_TEST)
		AVT2 = AVT.AVT(epsilon, beta, W2_I1, ITEM_VALUES_TEST)
		#print("--------------------------------END TABLES FOR " + str(user1.id) + ", " + str(user2.id) + "----------------\n\n")

		for key1, avo1 in AVT1.table.items():
			for key2, avo2 in AVT2.table.items():
				if beta 		<= avo1.ub / avo2.lb and \
					 1.0/beta >= avo1.ub / avo2.lb and \
					 beta 		<= avo2.ub / avo1.lb and \
					 1.0/beta >= avo2.ub / avo1.lb:

					# the tuples represent (user1_ID, user2_ID, receive_set_of_user1, receive_set_of_user2)
					#eligibleSwapsForUser1.add((user1.id, user2.id, avo1.ubi, avo2.lbi))
					if avo1.lb > gainUser1:
						maxSwapU1_U2 = (user1.id, user2.id, avo1.ubi, avo2.lbi)
						gainUser1 = avo1.lb

					#eligibleSwapsForUser2.add((user1.id, user2.id, avo1.lbi, avo2.ubi))
					if avo2.lb > gainUser2:
						maxSwapU2_U1 = (user2.id, user1.id, avo2.ubi, avo1.lbi)
						gainUser2 = avo2.lb

	# (max recommendation tuple for user1 to swap with user 2, max gain for user1 when swapping with user2, max recommendation for user2 to swap with user 1, ...)
	return (maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2)
