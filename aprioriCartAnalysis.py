import pandas as pd
import operator
import sys
from collections import Counter
from itertools import combinations

print("Reading data from File")
browsing_data = pd.read_csv("browsingData.csv",header = None)

browsing_data.head()
transactions = []
print("entering for loop to get all transactions")
for i in range(0, 31101):

    transactions.append([str(browsing_data.values[i,j]) for j in range(0, 28)])

frequencies = {}


print("Calculating frequencies")
for itemSet in transactions:
    for item in itemSet:
        if(item != " " and item != "nan"):
            if(item not in frequencies):
                frequencies[item] = 1
            else:
                frequencies[item]+=1



print("\nDone calculating frequencies\n")
frequent = {}
for value in frequencies:
    if(frequencies[value]>=100):
        #print("Passed support test value is: {}".format(value))
        #print("Adding to frequent set")
        frequent[value] = frequencies[value]

print("\n There are {}  frequent items boi".format(len(frequent)))
#Confidence = support of (x U y)/ support(x)


#Pruning
print("Pruning the transactions list of all transactions that do not contain frequent items")
prunedTransactions = []
pruned = 0
for itemSet in transactions:
    containsFrequent = False
    for item in itemSet:
        if(item in frequent):
            containsFrequent = True
    if(containsFrequent):
        prunedTransactions.append(itemSet)

    else:
        pruned+=1

print("There were {} transactions pruned and there are now {} transactions".format(pruned,len(prunedTransactions)))


#Making x,y tuples
pairs = combinations(frequent,2)






pairList = []
for x in pairs:
    pairList.append(x)

print("\n Now getting frequencies of each pair in the pruned transactions base \n")
pass2Frequencies = {}


pairFrequency = Counter()
for row in prunedTransactions:
    if (len(row)<2):
        continue
    row.sort()
    for tup in combinations(row,2):
        if("nan" not in tup):
            pairFrequency[tup] += 1



#Find ones that pass the Support
print("Find ones in second pass that pass the min support \n")
secondFrequent = {}
for value in pairFrequency:
    if(pairFrequency[value]>=100):
        #print("Passed support test value is: {}".format(value))
        #print("Adding to frequent set")
        secondFrequent[value] = pairFrequency[value]

print("\n There are {}  frequent pairs in the second pass boi".format(len(secondFrequent)))

rules = {}
print("\n Calculating Confidence scores now and ranking them \n")

for freqPair in secondFrequent:
    if("nan" not in freqPair):
        xConfidence = float(secondFrequent[freqPair]) / frequent[freqPair[0]]
        yConfidence = float(secondFrequent[freqPair]) / frequent[freqPair[1]]

        confidenceScore = max(xConfidence,yConfidence)

        rules[freqPair] = confidenceScore


print("Getting top five rules \n")

topFive = dict(sorted(rules.items(), key=operator.itemgetter(1), reverse=True)[:5])

print("The top five pairs are {}".format(topFive))
