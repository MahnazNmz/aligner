import optparse
import mlpy
import numpy as np

optparser = optparse.OptionParser()
optparser.add_option("-n", "--file", dest="fileName", default="pairs_withFeatures.txt", help="Each pair of sentences with pair features")
optparser.add_option("-e", "--english_pairs", dest="english_pairs", default="data/pairs.enu.dev", help="english pairs")
optparser.add_option("-f", "--foreign_pairs", dest="foreign_pairs", default="data/pairs.esn.dev", help="foreign pairs")
(opts, args) = optparser.parse_args()

paired_features = []
notpaired_features = []
paired = []
notpaired = []
truePairings = [(e.strip(), f.strip()) for (e,f) in zip(open(opts.english_pairs, "r"), open(opts.foreign_pairs, "r"))]

with open(opts.fileName, "r") as pairs:
	for line in pairs:
		(e, f, features) = line.split("|||")
		features = [float(feat) for feat in features.strip().split(" ")]
		if ((e.strip(),f.strip()) in truePairings):
			paired.append(1)
			paired_features.append(features)
		else:
			notpaired.append(-1)
			notpaired_features.append(features)


en = mlpy.ElasticNetC(lmb=0.01, eps=0.0001)
en.learn(np.concatenate((paired_features, notpaired_features), axis=0), np.concatenate((paired, notpaired)))
w = en.w()

print " ".join([str(weight) for weight in w])


