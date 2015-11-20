import multiprocessing as mp
import random
import string
from bookmoochData import *
import User

allUsers = list(set(WISHLISTS_TEST.keys()) | set(ITEMLISTS_TEST.keys()))[:10]

'''
def doInParallel(userId, append):
    return str(userId) + append
'''

def doInParallel(userId,
								itemlist,
								wishlist,
								itemvalues,
								ul,
								cl,
								wl,
								relativeWorth):

	return (userId, User.User(userId,
														itemlist,
														wishlist,
														itemvalues,
														ul,
														cl,
														wl,
														relativeWorth))


pool = mp.Pool(processes=4)
results = [pool.apply(doInParallel, args=(userId,
																					ITEMLISTS_TEST[userId],
																					WISHLISTS_TEST[userId],
																					ITEM_VALUES_TEST_i,
																					UL_TEST_i,
																					CL_TEST_i,
																					WL_TEST_i,
																					RELATIVE_WORTH_TEST_i,)) for userId in allUsers]
print(results)