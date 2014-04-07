import optparse

optparser = optparse.OptionParser()
optparser.add_option("-w", "--weights", dest="weights", default=None, help="3 numbers (weights) for each feature")
optparser.add_option("-f", "--file", dest="fileName", default="data/wiki_data/pairs_withFeatures.txt", help="Each pair of sentences with pair features")

weights = optparser.weights.split(" ")

with open(optparser.fileName, "r") as f:
	for line in f:
		(e, f, features) = f.split("|||")
		features = features.split(" ")
		classification = features[0]*weights[0]  + features[1]*weights[1] + features[2]*weights[2]
		if classification > 0:
			print e + " ||| " + f