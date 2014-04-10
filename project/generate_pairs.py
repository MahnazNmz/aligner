import optparse
import sys
optparser = optparse.OptionParser()
optparser.add_option("-w", "--weights", dest="weights", default=None, help="3 numbers (weights) for each feature")
optparser.add_option("-f", "--file", dest="fileName", default="pairs_withFeatures.test", help="Each pair of sentences with pair features")
(opts, args) = optparser.parse_args()

weights_file = sys.stdin if opts.weights is "-" else open(opts.weights)
weights = [float(w.strip()) for w in weights_file]

with open(opts.fileName, "r") as f:
	for line in f:
		(e, f, feat_strings) = line.split("|||")
		features = [float(feat) for feat in feat_strings.strip().split(" ")]
		classification = 0
		for index in range(0, len(weights)):
			classification += features[index]*weights[index]
		if classification > 0:
			print e + " ||| " + f