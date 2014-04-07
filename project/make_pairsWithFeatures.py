import optparse

optparser = optparse.OptionParser()
optparser.add_option("-ep", "--english_pairs", dest="english_pairs", default="data/wiki_data/pairs.enu.dev", help="english pairs")
optparser.add_option("-fp", "--foreign_pairs", dest="foreign_pairs", default="data/wiki_data/pairs.esn.dev", help="foreign pairs")

result = open("pairs_withFeatures.txt", "w")

with open(optparser.english_pairs, "r") as e:
	for line in e:
		with open(optparser.foreign_pairs, "")