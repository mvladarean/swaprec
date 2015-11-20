__author__ = 'Dih0r'

import csv
from progressbar import *
import pickle
from systemParameters import *

ITEM_VALUES_TEST_i = dict()
ITEMLISTS_TEST = dict()
WISHLISTS_TEST = dict()

UL_TEST_i = dict()
CL_TEST_i = dict()
WL_TEST_i = dict()
RELATIVE_WORTH_TEST_i = dict()

[ITEM_VALUES_TEST_i, UL_TEST_i, WL_TEST_i, ITEMLISTS_TEST, WISHLISTS_TEST, RELATIVE_WORTH_TEST_i] = pickle.load(open("invertedLists.pickle", "rb"))
print("Done reading")

'''
#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------REAL BOOKMOOCH DATA-------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
print("READING DATA FROM FILES...")
def computeRelativeValue(relativeWorth, itemValues, invertedListOfOwners):
	for itemId, itemValue in itemValues.items():
			if float(len(invertedListOfOwners[itemId])) != 0.0:
				relativeWorth[itemId] = float(itemValue) / float(len(invertedListOfOwners[itemId]))
			else:
				relativeWorth[itemId] = float("-inf")



itemsWithoutValues = 0
with open('data/datastore/datadump/1.0/price.csv', newline='\n') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		ITEM_VALUES_TEST[row[0]] = float(row[1])

		# for each item create an entry in the inverted lists
		UL_TEST[row[0]] = set()
		WL_TEST[row[0]] = set()

# AT THIS POINT ALL THE ITEMS WITH VALUES HAVE ENTRIES IN THE INVERTED LISTS

with open('data/datastore/datadump/1.0/item.csv', newline='\n') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		# put all items in the itemlist
		if row[0] in ITEMLISTS_TEST:
			ITEMLISTS_TEST[row[0]].add(row[1])
		else:
			ITEMLISTS_TEST[row[0]] = set()
			ITEMLISTS_TEST[row[0]].add(row[1])

		# check if the item exists in the list of values, if not, it needs an entry in all the inverted lists
		# as well as an associated value, since these things were not done in the first part
		if row[1] not in ITEM_VALUES_TEST:
			itemsWithoutValues += 1
			UL_TEST[row[1]] = set()
			WL_TEST[row[1]] = set()
			ITEM_VALUES_TEST[row[1]] = 1.0

		# Add to inverted lists
		UL_TEST[row[1]].add(row[0])


with open('data/datastore/datadump/1.0/wish.csv', newline='\n') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		if row[0] in WISHLISTS_TEST:
			WISHLISTS_TEST[row[0]].add(row[1])
		else:
			WISHLISTS_TEST[row[0]] = set()
			WISHLISTS_TEST[row[0]].add(row[1])

		# check if the item exists in the list of values, if not, it needs an entry in all the inverted lists
		# as well as an associated value, since these things were not done in the first part
		if row[1] not in ITEM_VALUES_TEST:
			itemsWithoutValues += 1
			UL_TEST[row[1]] = set()
			WL_TEST[row[1]] = set()
			ITEM_VALUES_TEST[row[1]] = 1.0

		# Add to inverted lists
		WL_TEST[row[1]].add(row[0])

# AT THIS POINT AL THE ITEMS IN THE WISHLISTS AND ITEMLISTS OF USERS HAVE BEEN ADDED TO THE INVERTED LISTS WL_TEST AND
# UL_TEST, AS WELL AS HAVE BEEN MADE AN ARTIFICIAL ENTRY IN THE VALUES STUFF => ALL THE USER ITEMS HAVE THE NEEDED
# INFO STORED ABOUT THEM IN THE INVERTE LISTS

print("DONE READING.")

#print("===" + str(itemsWithoutValues) + " out of " + str(itemsWithoutValues + len(ITEM_VALUES_TEST)))


RELATIVE_WORTH_TEST = {}
computeRelativeValue(RELATIVE_WORTH_TEST, ITEM_VALUES_TEST, UL_TEST)

usersWhoWish = set(WISHLISTS_TEST.keys())
usersWhoHave = set(ITEMLISTS_TEST.keys())
allUsers = usersWhoWish | usersWhoHave

onlyWish = usersWhoWish - usersWhoHave
onlyHave = usersWhoHave - usersWhoWish

print("FIXING LISTS...")
pbar = ProgressBar(
			widgets=[Percentage(), Bar()],
			maxval=len(allUsers)).start()

for i, userId in enumerate(allUsers):
	pbar.update(i + 1)

	if userId in usersWhoWish and userId in usersWhoHave:
		continue

	elif userId in onlyWish:
		ITEMLISTS_TEST[userId] = set()

	elif userId in onlyHave:
		WISHLISTS_TEST[userId] = set()

	else:
		continue

pbar.finish()

data = [ITEM_VALUES_TEST, UL_TEST, WL_TEST, ITEMLISTS_TEST, WISHLISTS_TEST, RELATIVE_WORTH_TEST]

with open('invertedLists.pickle', 'wb') as fp:
	pickle.dump(data, fp)
print("done wirting")
'''