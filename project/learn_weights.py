import optparse
import mlpy

optparser = optparse.OptionParser()
optparser.add_option("-f", "--file", dest="fileName", default="data/wiki_data/pairs_withFeatures.txt", help="Each pair of sentences with pair features")
optparser.add_option("-ep", "--english_pairs", dest="english_pairs", default="data/wiki_data/pairs.enu.dev", help="english pairs")
optparser.add_option("-fp", "--foreign_pairs", dest="foreign_pairs", default="data/wiki_data/pairs.esn.dev", help="foreign pairs")

featData = []
classifications = []
truePairings = zip(open(optparser.english_pairs, "r"), open(optparser.foreign_pairs, "r"))

with open(optparser.fileName, "r") as f:
	for line in f:
		(e, f, features) = f.split("|||")
		features = features.split(" ")
		featData.append(features)
		if (e,f in truePairings):
			classifications.append(1)
		else:
			classifications.append(-1)

en = mlpy.ElasticNetC(lmb=0.01, eps=0.0001)
en.learn(featData, classifications)
w = en.w()

print " ".join([str(weight) for weight in w])


