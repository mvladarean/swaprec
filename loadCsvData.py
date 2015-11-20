__author__ = 'Dih0r'

from DataFlowController import *

if DATA_FLOW_CONTROLLER == BOOKMOOCH_DATA_FLAG:
	from bookmoochData import *
else:
	from hardcodedData import *

from systemParameters import *

import User
from progressbar import *
from T1U2Exchange import *
import pickle
from pyspark import SparkContext, SparkConf
import multiprocessing as mp

def doInParallel(inputTuple):
	userId, itemlist, wishlist, itemvalues, ul, cl, wl, relativeWorth = inputTuple
	return (userId, User.User(userId,
														itemlist,
														wishlist,
														itemvalues,
														ul,
														cl,
														wl,
														relativeWorth))

if __name__ == "__main__":
	from bookmoochData import *
	from systemParameters import *
	import User
	from T1U2Exchange import *

	#USERS = pickle.load(open("userDict.pickle", "rb"))
	allUsers = set(WISHLISTS_TEST.keys()) | set(ITEMLISTS_TEST.keys())

	#SPARK IMPLEMENTATION
	conf = SparkConf().setAppName("topk").setMaster("local[4]")
	conf.set("spark.app.id", "topK")
	conf.set("spark.storage.memoryFraction", "0.15")
	conf.set("spark.kryoserializer.buffer.max", "512")
	conf.set("spark.driver.maxResultSize", "4g")
	sc = SparkContext(conf=conf)

	ITEM_VALUES_TEST = sc.broadcast(ITEM_VALUES_TEST_i)
	UL_TEST = sc.broadcast(UL_TEST_i)
	CL_TEST = sc.broadcast(CL_TEST_i)
	WL_TEST = sc.broadcast(WL_TEST_i)
	RELATIVE_WORTH_TEST = sc.broadcast(RELATIVE_WORTH_TEST_i)

	# CREATE USER SET
	print("MAKING USER SET")
	pool = mp.Pool()
	pbar = ProgressBar(
				widgets=[Percentage(), Bar()],
				maxval=len(allUsers)).start()

	USERS = dict()
	for i, userId in enumerate(allUsers):
		pbar.update(i + 1)
		wishList = WISHLISTS_TEST[userId]
		unneededItemList = ITEMLISTS_TEST[userId]

		USERS[userId] = User.User(userId,
															unneededItemList,
															wishList,
															ITEM_VALUES_TEST.value,
															UL_TEST.value,
															CL_TEST.value,
															WL_TEST.value,
															RELATIVE_WORTH_TEST.value)
		# This part also fills the inverted lists UL_TEST and CL_TEST

		if i == 50:
			break
	pbar.finish()
	print("FINISHED MAKING USER SET: " + str(sys.getsizeof(USERS)) + " bytes")

	'''

	# COMPUTE TOP 2 FOR EACH AT THIS INITIAL STEP => WILL UPDATE THE CRITICAL LISTS
	print("COMPUTING THE INITIAL RECOMMENDATIONS FOR " + str(len(USERS)) + " USERS.")

	pbar1 = ProgressBar(widgets=[Percentage(), Bar()],
											maxval=len(USERS)).start()
	i = 0
	n = len(USERS)
	for userId1, userObject1 in sorted(USERS.items(), key=lambda x: x[0]):
		pbar1.update(i + 1)

		print(str(i) + " out of " + str(n))
		for userId2, userObject2 in sorted(USERS.items(), key=lambda x: x[0]):
			#print("bla")
			if userId1 >= userId2:
				continue


			(maxSwapU1_U2, gainUser1, maxSwapU2_U1, gainUser2) = T1U2Exchange(userObject1, userObject2, EPSILON, BETA, ITEM_VALUES_TEST)

			if (gainUser1 == 0.0 and gainUser2 == 0.0):
				#print("+++++++ " + str(userObject1.id) + " - " + str(userObject2.id) + ": No viable exchange")
				#print()
				continue
			else:
				userObject1.insertOrUpdateTopk(maxSwapU1_U2, gainUser1)
				userObject2.insertOrUpdateTopk(maxSwapU2_U1, gainUser2)

				#print("+++++++ " + str(userObject1.id) + " - " + str(userObject2.id) + " SWAP:" + \
				#			userId1 + " - Recommendation: " + str(maxSwapU1_U2) + ", gain = " + str(gainUser1) + ", " + str(userId2) + \
				#			" - Recommendation: " + str(maxSwapU2_U1) + ", gain = " + str(gainUser2))
		i += 1

	pbar1.finish()
	'''


	#print(sorted(USERS.items(), key=lambda x: x[0]))

	distributedUsersList = sc.parallelize(sorted(USERS.items(), key=lambda x: x[0]), 10)
	#distributedUsersList = sc.parallelize(sorted(USERS.keys()), 10)
	print("bla bla")

	resultingRecommendations = distributedUsersList.cartesian(distributedUsersList) \
																							   .filter(lambda pairId: int(pairId[0][0]) % 2  == 0)
																								 #.flatMap(lambda pairId: pairId) \

																								 #\
																								 #.collect()
	print(resultingRecommendations.take(100))
	print("SUCCEEEEEEEESSSSSS")
	'''
																								 # \
																								 #.filter(lambda pairOfUsers: (pairOfUsers[0][0] < pairOfUsers[1][0]) and (T1U2Exchange(pairOfUsers[0][1], pairOfUsers[1][1], EPSILON, BETA)[1] != 0.0)) \
																								 # \

	'''

	print("chacha")
	'''
	with open('initialRecommendations.pickle', 'wb') as fp:
		pickle.dump(resultingRecommendations, fp)
	print("done writing recommendations to file")
	'''