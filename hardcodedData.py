__author__ = 'Dih0r'
import csv
from progressbar import *

#BASED ON TABLE 3
userNo = 5

ITEM_VALUES_FOR_AVT = {"i1": 2, "i2": 2, "i3": 3}

UL = {"i1": {"u3", "u5"}, "i2": {"u3"}, "i3": {"u2", "u5"}, "i4": {"u1"}, "i5": {"u1", "u2"}, "i6": {"u1", "u3", "u4"}}

CL = {"u1": {"i1", "i2"}, "u2": {"i2"}, "u3": {"i5"}, "u4": {"i1", "i4"}, "u5": {"i4", "i6"}}

ITEM_VALUES = {"i1": 70, "i2": 40, "i3": 20, "i4": 35, "i5": 80, "i6": 10}
WISHLISTS = {"u1": {"i1", "i2", "i3"}, "u2": {"i2", "i6"}, "u3": {"i3", "i5"}, "u4": {"i1", "i4"}, "u5": {"i4", "i6"}}
ITEMLISTS = {"u1": {"i4", "i5", "i6"}, "u2": {"i3", "i5"}, "u3": {"i1", "i2", "i6"}, "u4": {"i6"}, "u5": {"i1", "i3"}}
TOPK = {"u1": {"i4", "i5", "i6"}, "u2": {"i3", "i5"}, "u3": {"i1", "i2", "i6"}, "u4": {"i6"}, "u5": {"i1", "i3"}} # TO BE MODIFIED
CURRENT_GAIN = {"u1": 60, "u2": 50, "u3": 80, "u4": 0, "u5": 10}
RELATIVE_WORTH = {}


def computeRelativeValue(relativeWorth, itemValues, invertedListOfOwners):
	for itemId, itemValue in itemValues.items():
			if float(len(invertedListOfOwners[itemId])) != 0.0:
				relativeWorth[itemId] = float(itemValue) / float(len(invertedListOfOwners[itemId]))
			else:
				relativeWorth[itemId] = float("-inf")

computeRelativeValue(RELATIVE_WORTH, ITEM_VALUES, UL)



#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------EXAMPLE FIGURE 3----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

ITEM_VALUES_TEST = {"i1": 10, "i2": 20, "i3": 70, "i4": 80, "i5": 100, "i6": 170} #{"i1": 70, "i2": 40, "i3": 20, "i4": 35, "i5": 80, "i6": 10} #RESTORE:
WISHLISTS_TEST = {"u1": {"i2", "i3"}, "u2": {"i1", "i6"}, "u3": {"i4", "i5"}} #{"u1": {"i1", "i2", "i3"}, "u2": {"i2", "i6"}, "u3": {"i3", "i5"}, "u4": {"i1", "i4"}, "u5": {"i4", "i6"}} #RESTORE:
ITEMLISTS_TEST = {"u1": {"i4", "i1"}, "u2": {"i4", "i5"}, "u3": {"i2", "i3", "i6"}} #{"u1": {"i4", "i5", "i6"}, "u2": {"i3", "i5"}, "u3": {"i1", "i2", "i6"}, "u4": {"i6"}, "u5": {"i1", "i3"}} #RESTORE:
UL_TEST = {"i1": set(), "i2": set(), "i3": set(), "i4": set(), "i5": set(), "i6": set()}
CL_TEST = {"i1": set(), "i2": set(), "i3": set(), "i4": set(), "i5": set(), "i6": set()}
WL_TEST = {"i1": set(), "i2": set(), "i3": set(), "i4": set(), "i5": set(), "i6": set()}

# Will be filled by the function below
RELATIVE_WORTH_TEST = {}
computeRelativeValue(RELATIVE_WORTH_TEST, ITEM_VALUES_TEST, UL_TEST)



