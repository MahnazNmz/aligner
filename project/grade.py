import sys

engFile = open("test/pairs.enu.test", "r")
spanFile = open("test/pairs.esn.test", "r")

humanPairings = zip([line.strip() for line in engFile], [line.strip() for line in spanFile])

correct = 0
totalOutputted = 0

for line in sys.stdin:
	totalOutputted += 1
	english, spanish = (sent.strip() for sent in line.split(" ||| "))
	if (english, spanish) in humanPairings:
		correct += 1

f1 = -1

if correct == 0:
	f1 = float("inf")
elif totalOutputted != 0:
	precision = float(correct) / totalOutputted
	recall = float(correct) / len(humanPairings)
	f1 = float(2) * float(precision + recall)/float(precision * recall)

print f1