import optparse
import mlpy
import numpy as np

optparser = optparse.OptionParser()
optparser.add_option("-n", "--file", dest="fileName", default="pairs_withFeatures.dev", help="Each pair of sentences with pair features")
optparser.add_option("-e", "--english_pairs", dest="english_pairs", default="data/pairs.enu.dev", help="english pairs")
optparser.add_option("-f", "--foreign_pairs", dest="foreign_pairs", default="data/pairs.esn.dev", help="foreign pairs")
(opts, args) = optparser.parse_args()

featData = []
pairs_feat = []
nonepairs_feat = []
pairs_category = []
nonepairs_category = []
truePairings = [(e.strip(), f.strip()) for (e,f) in zip(open(opts.english_pairs, "r"), open(opts.foreign_pairs, "r"))]


with open(opts.fileName, "r") as pairs:
	i = 1
	for line in pairs:
		(e, f, features) = line.split("|||")
		features = [float(feat) for feat in features.strip().split(" ")]
		if ((e.strip(),f.strip()) in truePairings):
			pairs_feat.append(features)
			pairs_category.append(1)
		else:
			if i % 50 == 0 or features[5] != 0:
				nonepairs_feat.append(features)
				nonepairs_category.append(-1)
				
		i+=1


x = np.concatenate((pairs_feat, nonepairs_feat), axis = 0)
y = np.concatenate((pairs_category, nonepairs_category))
p = mlpy.Perceptron(alpha=0.1, thr=0.05, maxiters=100) # basic perceptron
p.learn(x, y)
w = p.w()

print "\n".join([str(weights) for weights in w])


