__author__ = 'Dih0r'

from systemParameters import *
from T1U2Exchange import *


def deleteItem(updateUserId,
							 userBase,
							 wishlistOrItemlist,
							 itemId,
							 ITEM_VALUES_TEST):

	assert itemId in ITEM_VALUES_TEST, "ERROR: Item to delete not in the database."

	if wishlistOrItemlist == CHECK_WISHLIST:
		userBase[updateUserId].deleteItemFromWishlist(itemId, userBase)

	elif wishlistOrItemlist == CHECK_ITEMLIST:
		userBase[updateUserId].deleteItemFromItemlist(itemId, userBase)

	else:
		print("EEEEEEEEEEEERRRRRRRRROOOOOOOORRRRRRRRRR. Third paraeter needs to be 0 or 1")

